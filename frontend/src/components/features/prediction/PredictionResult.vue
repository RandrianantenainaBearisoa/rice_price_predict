<template>
    <div class="result-container">
        <h3>Prediction Result</h3>
        <div class="result-content">
            <pre>{{ JSON.stringify(result, null, 2) }}</pre>
        </div>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    result: any;
}>();
</script>

<style scoped>
.result-container {
    margin-top: 2rem;
    padding: 1.5rem;
    background-color: var(--color-bg-lighter);
    border-radius: 4px;
    border-left: 4px solid var(--color-accent);
}

.result-container h3 {
    margin-top: 0;
    color: var(--color-text-primary);
    margin-bottom: 1rem;
}

.result-content {
    background-color: var(--color-bg-white);
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
}

.result-content pre {
    margin: 0;
    font-size: 0.9rem;
    color: var(--color-text-primary);
}
</style>
