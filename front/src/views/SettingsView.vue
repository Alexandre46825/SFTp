<template>
  <div class="max-w-3xl">
    <h2 class="text-3xl font-bold mb-6">
      Paramètres
    </h2>

    <div class="space-y-6">
      <div class="bg-slate-800 p-6 rounded-xl border border-slate-700">
        <h3 class="text-xl font-semibold mb-4">
          Profil
        </h3>

        <div class="space-y-4">
          <input
            type="text"
            placeholder="Nom d'utilisateur"
            class="w-full rounded-lg bg-slate-900 border border-slate-700 p-3"
          >

          <input
            type="email"
            placeholder="Adresse e-mail"
            class="w-full rounded-lg bg-slate-900 border border-slate-700 p-3"
          >
        </div>
      </div>

      <div class="bg-slate-800 p-6 rounded-xl border border-slate-700">
        <h3 class="text-xl font-semibold mb-4">
          Préférences
        </h3>

        <div class="space-y-4">
          <label class="flex items-center gap-3">
            <input type="checkbox">

            <span>Recevoir les notifications</span>
          </label>

          <label class="flex items-center gap-3">
            <input type="checkbox">

            <span>Activer le mode sombre</span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>