export interface SchemaProperty {
    $ref?: string;
    type?: string;
    title?: string;
    enum?: any[];
    exclusiveMinimum?: number;
}

export interface SchemaDef {
    enum?: any[];
    title?: string;
    type?: string;
}

export interface Schema {
    $defs?: Record<string, SchemaDef>;
    properties: Record<string, SchemaProperty>;
    required?: string[];
}

export interface FormField {
    key: string;
    label: string;
    type: 'text' | 'number' | 'select';
    required: boolean;
    options?: { value: string; label: string[] }[];
    min?: number;
}