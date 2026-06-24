<template>
  <div>
    <h2 class="text-3xl font-bold mb-6">
      Mes fichiers
    </h2>

    <div class="overflow-hidden rounded-xl border border-slate-700">
      <div class="overflow-x-auto">
      <table class="w-full text-left min-w-[700px]">
        <thead class="bg-white dark:bg-gray-800">
          <tr>
            <th class="p-4">Nom</th>
            <th class="p-4">Taille</th>
            <th class="p-4">Date</th>
            <th class="p-4">Statut</th>
          </tr>
        </thead>

        <tbody>
          <tr class="border-t border-slate-700 hover:bg-white dark:bg-gray-800">
            <td class="p-4">rapport.pdf</td>
            <td class="p-4">2,4 Mo</td>
            <td class="p-4">16/06/2026</td>
            <td class="p-4 text-green-400">Envoyé</td>
          </tr>

          <tr class="border-t border-slate-700 hover:bg-white dark:bg-gray-800">
            <td class="p-4">images.zip</td>
            <td class="p-4">150 Mo</td>
            <td class="p-4">15/06/2026</td>
            <td class="p-4 text-yellow-400">En attente</td>
          </tr>
        </tbody>
      </table>
      </div>
    </div>
  </div>
</template>