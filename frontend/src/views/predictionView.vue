<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { publicLayout } from '@/components/layouts';
import { getFeatures, sendEntry } from '@/static/apis';
import { LoadingState, ErrorAlert } from '@/components/ui';
import { PredictionFormField, PredictionResult } from '@/components/features/prediction';
import PrimaryButton from '@/components/ui/buttons/PrimaryButton.vue';
import type { FormField as FormFieldInterface } from '@/static/interfaces';

const fields = ref<FormFieldInterface[]>([]);
const formData = ref<Record<string, unknown>>({});
const loading = ref(false);
const error = ref<string | null>(null);
const result = ref<any>(null);

onMounted(async () => {
    loading.value = true;
    try {
        const result = await getFeatures();
        fields.value = result.filter((field: FormFieldInterface) => field.required);
        // Initialize formData with empty values for required fields only
        fields.value.forEach((field) => {
            formData.value[field.key] = '';
        });
    } catch (err) {
        error.value = 'Failed to load form fields';
        console.error(err);
    } finally {
        loading.value = false;
    }
});

const handleSubmit = async () => {
    // Validate required fields
    const missingRequired = fields.value.filter((field) => field.required && !formData.value[field.key]);
    if (missingRequired.length > 0) {
        error.value = `Please fill in all required fields: ${missingRequired.map((f) => f.label).join(', ')}`;
        return;
    }

    loading.value = true;
    error.value = null;
    result.value = null;
    try {
        // Send only required fields
        const dataToSend = Object.fromEntries(
            Object.entries(formData.value).filter(([key]) =>
                fields.value.some((field) => field.key === key && field.required)
            )
        );
        const response = await sendEntry(dataToSend);
        result.value = response;
        console.log('Prediction result:', response);
    } catch (err) {
        error.value = 'Failed to send prediction request';
        console.error(err);
    } finally {
        loading.value = false;
    }
};
</script>

<template>
    <div>
        <publicLayout pageTitle="Prediction">
            <div class="prediction-form-container">
                <!-- Loading State -->
                <LoadingState v-if="loading" message="Loading form fields..." />

                <!-- Error Message -->
                <ErrorAlert v-if="error" :message="error" />

                <!-- Form -->
                <form v-if="!loading && fields.length > 0" @submit.prevent="handleSubmit" class="form-grid">
                    <PredictionFormField
                        v-for="field in fields"
                        :key="field.key"
                        :field="field"
                        :modelValue="formData[field.key]"
                        @update:modelValue="formData[field.key] = $event"
                    />

                    <!-- Submit Button -->
                    <PrimaryButton
                        :text="loading ? 'Sending...' : 'Get Prediction'"
                        :disabled="loading"
                        type="submit"
                        @click="handleSubmit"
                    />
                </form>

                <!-- Result Section -->
                <PredictionResult v-if="result" :result="result" />
            </div>
        </publicLayout>
    </div>
</template>

<style scoped>
.prediction-form-container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.form-grid button {
    grid-column: 1 / -1;
}
</style>