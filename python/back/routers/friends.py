from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import User, Friendship
from schemas import FriendshipCreate, FriendInfo, FriendRequestInfo

router = APIRouter()


@router.post("/add", response_model=FriendInfo)
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

    return receiver


@router.get("/requests", response_model=list[FriendRequestInfo])
def get_friend_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    requests = db.query(Friendship).filter(
        Friendship.id_receiver == current_user.id_user,
        Friendship.status == "pending"
    ).all()

    requesters = []
    for req in requests:
        requester = db.query(User).filter(User.id_user == req.id_requester).first()
        if requester:
            requesters.append(requester)

    return requesters


@router.get("/list", response_model=list[FriendInfo])
def get_friends(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friendships = db.query(Friendship).filter(
        (Friendship.id_requester == current_user.id_user) |
        (Friendship.id_receiver == current_user.id_user),
        Friendship.status == "accepted"
    ).all()

    friends_list = []
    for friendship in friendships:
        if friendship.id_requester == current_user.id_user:
            friend_id = friendship.id_receiver
        else:
            friend_id = friendship.id_requester

        friend = db.query(User).filter(User.id_user == friend_id).first()
        if friend:
            friends_list.append(friend)

    return friends_list


@router.get("/list/{user_id}", response_model=list[FriendInfo])
def get_friends_of_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès admin requis")

    target_user = db.query(User).filter(User.id_user == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    friendships = db.query(Friendship).filter(
        (Friendship.id_requester == user_id) |
        (Friendship.id_receiver == user_id),
        Friendship.status == "accepted"
    ).all()

    friends_list = []
    for friendship in friendships:
        if friendship.id_requester == user_id:
            friend_id = friendship.id_receiver
        else:
            friend_id = friendship.id_requester

        friend = db.query(User).filter(User.id_user == friend_id).first()
        if friend:
            friends_list.append(friend)

    return friends_list


@router.put("/accept/{user_id}", response_model=FriendInfo)
def accept_friend(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friendship = db.query(Friendship).filter(
        Friendship.id_requester == user_id,
        Friendship.id_receiver == current_user.id_user,
        Friendship.status == "pending"
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Demande introuvable")

    friendship.status = "accepted"
    db.commit()

    requester = db.query(User).filter(User.id_user == user_id).first()
    return requester


@router.put("/block/{user_id}", response_model=FriendInfo)
def block_friend(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friendship = db.query(Friendship).filter(
        Friendship.id_requester == user_id,
        Friendship.id_receiver == current_user.id_user
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Demande introuvable")

    friendship.status = "blocked"
    db.commit()

    requester = db.query(User).filter(User.id_user == user_id).first()
    return requester


@router.delete("/remove/{user_id}")
def remove_friend(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    friendship = db.query(Friendship).filter(
        ((Friendship.id_requester == current_user.id_user) & (Friendship.id_receiver == user_id)) |
        ((Friendship.id_requester == user_id) & (Friendship.id_receiver == current_user.id_user))
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Amitié introuvable")

    db.delete(friendship)
    db.commit()
    return {"message": "Ami supprimé"}