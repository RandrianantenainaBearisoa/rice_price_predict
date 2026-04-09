<template>
    <div class="error-message">
        {{ message }}
    </div>
</template>

<script setup lang="ts">
defineProps<{
    message: string;
}>();
</script>

<style scoped>
.error-message {
    padding: 1rem;
    background-color: var(--color-error-bg);
    color: var(--color-error-text);
    border-radius: 4px;
    margin-bottom: 1rem;
}
</style>
