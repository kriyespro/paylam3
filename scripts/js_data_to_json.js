// One-off extractor: turns a legacy `const xDatabase = [...]` content file into
// JSON on stdout, so the Django import_subjects command can read it without a
// JS parser dependency in Python. Not part of the app runtime.
//
// Usage: node scripts/js_data_to_json.js <path-to-data.js> <varName>

const fs = require('fs');

const [, , filePath, varName] = process.argv;

if (!filePath || !varName) {
    console.error('Usage: node js_data_to_json.js <file.js> <varName>');
    process.exit(1);
}

const source = fs.readFileSync(filePath, 'utf8');

// Some legacy files (api.js) have top-level side effects that touch
// browser-only globals (localStorage, window). Stub them so extraction
// doesn't crash on code we don't care about here — we only want the data
// array, and letting the stub silently absorb writes is harmless.
const localStorageStub = (() => {
    const store = {};
    return {
        getItem: (k) => (k in store ? store[k] : null),
        setItem: (k, v) => { store[k] = String(v); },
        removeItem: (k) => { delete store[k]; },
    };
})();

// `const` scopes to the Function body, so evaluating the whole file inside
// a Function and returning the variable by name gives us the array back
// without needing module.exports in the legacy file.
const extract = new Function(
    'localStorage', 'window', 'document',
    `${source}\nreturn ${varName};`,
);
const data = extract(localStorageStub, {}, {});

process.stdout.write(JSON.stringify(data));
