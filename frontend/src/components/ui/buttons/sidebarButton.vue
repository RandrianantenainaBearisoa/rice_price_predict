<template>
    <div class="side-bar-button">
        <router-link :to="{ name: routeName}">
            <div class="side-button-label">
                {{ label }}
            </div>
        </router-link>
    </div>
</template>

<script lang="ts">
export default {
    props: {
        label: String,
        routeName: String
    }
}
</script>

<style lang="scss">
.side-bar-button {
    width: 100%;

    a {
        text-decoration-line: none;
    }

    .router-link-active {
        font-weight: bold;
        text-decoration: underline var(--font-color-00);
    }

    .side-button-label {
        width: 90%;
        padding: 5px;
        border-radius: 5px;
        text-align: center;
        color: var(--font-color-00);
        transition: all 0.1s ease-in-out 0.1s;
        background-color: var(--background-color-00);
        border: var(--background-color-00) solid 1px;

        &:hover{
            border: var(--font-color-00) solid 1px;
        }
    }
}
</style>