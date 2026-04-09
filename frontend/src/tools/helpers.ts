import { type Schema, type SchemaDef, type SchemaProperty, type FormField } from '@/static/interfaces';

function resolveRef(schema: Schema, ref: string): SchemaDef | null {
    const path = ref.replace('#/$defs/', '');
    return schema.$defs?.[path] || null;
}

function extractOptions(def: SchemaDef): { value: string; label: string[] }[] | null {
    if (!def.enum) return null;
    if (Array.isArray(def.enum) && typeof def.enum[0] === 'string') {
        return def.enum.map((item: string) => ({ value: item, label: [item] }));
    }
    if (Array.isArray(def.enum) && typeof def.enum[0] === 'object') {
        return def.enum.map((item: any) => ({
            value: item.value,
            label: item.labels ? Object.values(item.labels) : [item.feature || item.value],
        }));
    }
    return null;
}

function getFieldType(prop: SchemaProperty): 'text' | 'number' | 'select' {
    if (prop.type === 'number') return 'number';
    if (prop.$ref) return 'select';
    return 'text';
}

export function schemaToFormFields(schema: Schema): FormField[] {
    const fields: FormField[] = [];
    const requiredSet = new Set(schema.required || []);

    for (const [key, prop] of Object.entries(schema.properties)) {
        const field: FormField = {
            key,
            label: prop.title || key,
            type: getFieldType(prop),
            required: requiredSet.has(key),
        };

        if (prop.type === 'number' && prop.exclusiveMinimum !== undefined) {
            field.min = prop.exclusiveMinimum;
        }

        if (prop.$ref) {
            const def = resolveRef(schema, prop.$ref);
            if (def) {
                field.options = extractOptions(def) || [];
            }
        }

        fields.push(field);
    }

    return fields;
}