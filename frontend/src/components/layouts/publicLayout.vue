<script setup>
import sidebarLayout from './sidebarLayout.vue';
import { logo } from '../ui';
</script>

<template>
    <div class="global-content-wrapper">
        <aside class="side-wrapper">
            <div class="logo-container">
                <logo />
            </div>
            <div class="sidebar-container">
                <sidebarLayout />
            </div>
        </aside>
        <div class="view-wrapper">
            <div class="view-title">
                <h1>
                    {{ pageTitle }}
                </h1>
            </div>
            <div class="view-content">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        pageTitle: String
    }
}
</script>

<style scoped>
.global-content-wrapper {
    display: flex;
    width: 100%;
    height: 100%;
    margin: auto;
    background-color: var(--background-color-00);

    .side-wrapper {
        width: 15%;
        display: flex;
        flex-direction: column;

        .logo-container {
            height: 15%;
        }
        .sidebar-container {
            height: 85%;
        }
    }

    .view-wrapper {
        width: 85%;
        display: flex;
        flex-direction: column;

        .view-title {
            height: 15%;
            display: flex;
            justify-content: center;
            align-items: center;
            color: var(--font-color-00);
            background-color: var(--background-color-00);
        }
        .view-content {
            height: 85%;
        }
    }
}
</style>