<template>
    <div class="form-group">
        <!-- Label -->
        <label :for="field.key" class="form-label">
            {{ firstLetterUpperCase(field.label) }}
            <span v-if="field.required" class="required">*</span>
        </label>

        <!-- Text Input -->
        <input
            v-if="field.type === 'text'"
            :id="field.key"
            :value="modelValue"
            @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
            type="text"
            required
            class="form-input"
            :placeholder="`Enter ${field.label}`"
        />

        <!-- Number Input -->
        <input
            v-if="field.type === 'number'"
            :id="field.key"
            :value="modelValue"
            @input="$emit('update:modelValue', parseFloat(($event.target as HTMLInputElement).value) || '')"
            type="number"
            step="0.01"
            required
            :min="field.min"
            class="form-input"
            :placeholder="`Enter ${field.label}`"
        />

        <!-- Select Input -->
        <select
            v-if="field.type === 'select'"
            :id="field.key"
            :value="modelValue"
            @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
            required
            class="form-input"
        >
            <option value="" disabled>
                Select {{ firstLetterUpperCase(field.label) }}
            </option>
            <option v-for="option in field.options" :key="option.value" :value="option.value">
                {{ option.label[0] }}
            </option>
        </select>
    </div>
</template>

<script setup lang="ts">
import { firstLetterUpperCase } from '@/tools/utils';
import type { FormField } from '@/static/interfaces';

defineProps<{
    field: FormField;
    modelValue: any;
}>();

defineEmits<{
    'update:modelValue': [value: any];
}>();
</script>

<style scoped>
.form-group {
    display: flex;
    flex-direction: column;
}

.form-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #333;
}

.required {
    color: red;
    margin-left: 0.25rem;
}

.form-input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    box-sizing: border-box;
}

.form-input:focus {
    outline: none;
    border-color: #4caf50;
    box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
}
</style>
