from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import User, Friendship
from schemas import FriendshipCreate, FriendshipOut

router = APIRouter()


@router.post("/add", response_model=FriendshipOut)
def add_friend(
    data: FriendshipCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    receiver = db.query(User).filter(User.id_user == data.id_receiver).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    if data.id_receiver == current_user.id_user:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas vous ajouter vous-même")

    existing = db.query(Friendship).filter(
        Friendship.id_requester == current_user.id_user,
        Friendship.id_receiver == data.id_receiver
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Demande déjà envoyée")

    new_friendship = Friendship(
        id_requester=current_user.id_user,
        id_receiver=data.id_receiver,
        status="pending"
    )
    db.add(new_friendship)
    db.commit()
    db.refresh(new_friendship)
    return new_friendship


@router.get("/requests", response_model=list[FriendshipOut])
def get_friend_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    requests = db.query(Friendship).filter(
        Friendship.id_receiver == current_user.id_user,
        Friendship.status == "pending"
    ).all()
    return requests


@router.get("/list", response_model=list[FriendshipOut])
def get_friends(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friends = db.query(Friendship).filter(
        (Friendship.id_requester == current_user.id_user) |
        (Friendship.id_receiver == current_user.id_user),
        Friendship.status == "accepted"
    ).all()
    return friends


@router.put("/accept/{friendship_id}", response_model=FriendshipOut)
def accept_friend(
    friendship_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friendship = db.query(Friendship).filter(
        Friendship.id_friendship == friendship_id,
        Friendship.id_receiver == current_user.id_user,
        Friendship.status == "pending"
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Demande introuvable")

    friendship.status = "accepted"
    db.commit()
    db.refresh(friendship)
    return friendship


@router.put("/block/{friendship_id}", response_model=FriendshipOut)
def block_friend(
    friendship_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friendship = db.query(Friendship).filter(
        Friendship.id_friendship == friendship_id,
        Friendship.id_receiver == current_user.id_user
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Demande introuvable")

    friendship.status = "blocked"
    db.commit()
    db.refresh(friendship)
    return friendship


@router.delete("/remove/{friendship_id}")
def remove_friend(
    friendship_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friendship = db.query(Friendship).filter(
        Friendship.id_friendship == friendship_id,
        (Friendship.id_requester == current_user.id_user) |
        (Friendship.id_receiver == current_user.id_user)
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Amitié introuvable")

    db.delete(friendship)
    db.commit()
    return {"message": "Ami supprimé"}