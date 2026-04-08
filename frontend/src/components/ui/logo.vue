<template>
    <router-link :to="{name: 'home'}">
        <div class="image-container">
                <img src="/assets/images/logo.png" alt="APP_LOGO">
        </div>
    </router-link>
</template>

<style lang="scss">
.image-container {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

div img {
    height: 100%;
}
</style>