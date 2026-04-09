<template>
    <section class="description">
        <div class="description-card">
            <h2>{{ title }}</h2>
            <p>{{ content }}</p>
        </div>
    </section>
</template>

<script setup lang="ts">
defineProps<{
    title: string;
    content: string;
}>();
</script>

<style scoped>
.description {
    margin-bottom: 3rem;
}

.description-card {
    background-color: #f9f9f9;
    padding: 2rem;
    border-radius: 8px;
    border-left: 4px solid #4caf50;
}

.description-card h2 {
    margin-top: 0;
    color: #333;
}

.description-card p {
    color: #666;
    line-height: 1.6;
    margin: 0;
}
</style>
