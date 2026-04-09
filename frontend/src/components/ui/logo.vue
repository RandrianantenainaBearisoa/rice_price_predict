<template>
    <div class="image-container">
            <router-link :to="{name: 'home'}">
                <img src="/assets/images/logo.png" alt="APP_LOGO">
            </router-link>
        </div>
</template>

<style lang="scss">
a {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.image-container {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

div img {
    // width: 90%;
    height: 90%;
    border: var(--font-color-00) solid 1px;
    border-radius: 100%;;
}
</style>