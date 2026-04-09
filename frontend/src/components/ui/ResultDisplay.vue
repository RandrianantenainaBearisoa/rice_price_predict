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
    background-color: #f5f5f5;
    border-radius: 4px;
    border-left: 4px solid #4caf50;
}

.result-container h3 {
    margin-top: 0;
    color: #333;
    margin-bottom: 1rem;
}

.result-content {
    background-color: white;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
}

.result-content pre {
    margin: 0;
    font-size: 0.9rem;
    color: #333;
}
</style>
