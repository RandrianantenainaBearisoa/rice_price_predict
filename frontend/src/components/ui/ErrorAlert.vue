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
    background-color: #ffebee;
    color: #c62828;
    border-radius: 4px;
    margin-bottom: 1rem;
}
</style>
