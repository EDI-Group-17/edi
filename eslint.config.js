import js from "@eslint/js";

export default [
    js.configs.recommended,
    {
        files: ["**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx"],
        ignores: ["node_modules/**", "dist/**", "build/**"],
        rules: {
            "no-unused-vars": "warn",
            "no-undef": "error",
            "react/react-in-jsx-scope": "off",
        },
        languageOptions: {
            ecmaVersion: "latest",
            sourceType: "module",
            globals: {
                window: "readonly",
                document: "readonly",
                console: "readonly",
                process: "readonly"
            }
        }
    }
];
