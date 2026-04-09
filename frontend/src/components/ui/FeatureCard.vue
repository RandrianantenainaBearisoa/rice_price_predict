<template>
    <div class="feature-card">
        <div class="feature-icon">{{ icon }}</div>
        <h3>{{ title }}</h3>
        <p>{{ description }}</p>
    </div>
</template>

<script setup lang="ts">
defineProps<{
    icon: string;
    title: string;
    description: string;
}>();
</script>

<style scoped>
.feature-card {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    border: 1px solid #eee;
    transition: box-shadow 0.3s ease;
}

.feature-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.feature-card h3 {
    color: #333;
    margin: 1rem 0 0.5rem;
}

.feature-card p {
    color: #666;
    font-size: 0.95rem;
    line-height: 1.5;
    margin: 0;
}
</style>
