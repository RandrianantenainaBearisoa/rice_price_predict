<script setup lang="ts">
import { sidebarButton } from '../ui';
</script>

<template>
    <div class="sidebar-button-wrapper">
        <sidebarButton label="Prediction" route-name="predict"/>
        <sidebarButton label="Home" route-name="home" />
    </div>
</template>

<style scoped lang="scss">
.sidebar-button-wrapper {
    height: 98%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 5px;
    gap: 5px;
    background-color: var(--background-color-01);
}
</style>