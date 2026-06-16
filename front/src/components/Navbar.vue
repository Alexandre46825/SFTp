<template>
    <header class="h-16 bg-slate-800 border-b border-slate-700 px-6 flex items-center justify-between">
        <h1 class="text-xl font-bold text-white">
            <img src="/img/logo.png" alt="Logo" class="inline-block h-8 mr-2">
            SFTP
        </h1>

        <nav>
            <ul class="flex gap-6 text-slate-300">
                <RouterLink
                    to="/notifications"
                    class="hover:text-blue-400 transition"
                    >
                    Notifications
                </RouterLink>
                <RouterLink
                    to="/settings"
                    class="hover:text-blue-400 transition"
                    >
                    Account
                </RouterLink>
            </ul>
        </nav>
    </header> 
</template>