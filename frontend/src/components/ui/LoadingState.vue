<template>
    <div class="loading">
        {{ message }}
    </div>
</template>

<script setup lang="ts">
defineProps<{
    message?: string;
}>();
</script>

<style scoped>
.loading {
    text-align: center;
    padding: 2rem;
    color: var(--color-text-secondary);
}
</style>
