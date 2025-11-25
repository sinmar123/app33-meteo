/*
 * SCRIPT DI ANALISI PAGINA METEO
 *
 * COME USARE:
 * 1. Apri: https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteo.asp
 * 2. Premi F12 (apri DevTools)
 * 3. Vai su "Console"
 * 4. Copia e incolla TUTTO questo script
 * 5. Premi INVIO
 * 6. Copia l'output che appare
 * 7. Incollalo nella chat
 */

console.log("==========================================");
console.log("ANALISI PAGINA METEO - REGIONE LIGURIA");
console.log("==========================================\n");

// Trova tutti i SELECT
const selects = document.querySelectorAll('select');
console.log(`Trovati ${selects.length} elementi SELECT:\n`);

selects.forEach((select, index) => {
    console.log(`\n--- SELECT #${index + 1} ---`);
    console.log(`ID: ${select.id || 'N/A'}`);
    console.log(`NAME: ${select.name || 'N/A'}`);
    console.log(`Numero opzioni: ${select.options.length}`);

    // Mostra prime 3 opzioni come esempio
    console.log('Prime 3 opzioni:');
    for(let i = 0; i < Math.min(3, select.options.length); i++) {
        console.log(`  [${i}] value="${select.options[i].value}" → ${select.options[i].text}`);
    }
});

// Trova tutti gli INPUT
const inputs = document.querySelectorAll('input[type="text"], input[type="date"]');
console.log(`\n\nTrovati ${inputs.length} elementi INPUT:\n`);

inputs.forEach((input, index) => {
    console.log(`\n--- INPUT #${index + 1} ---`);
    console.log(`ID: ${input.id || 'N/A'}`);
    console.log(`NAME: ${input.name || 'N/A'}`);
    console.log(`TYPE: ${input.type}`);
    console.log(`PLACEHOLDER: ${input.placeholder || 'N/A'}`);
});

// Trova tutti i BUTTON/SUBMIT
const buttons = document.querySelectorAll('button, input[type="submit"], input[type="button"]');
console.log(`\n\nTrovati ${buttons.length} elementi BUTTON:\n`);

buttons.forEach((button, index) => {
    console.log(`\n--- BUTTON #${index + 1} ---`);
    console.log(`ID: ${button.id || 'N/A'}`);
    console.log(`NAME: ${button.name || 'N/A'}`);
    console.log(`TYPE: ${button.type || 'N/A'}`);
    console.log(`VALUE: ${button.value || 'N/A'}`);
    console.log(`TEXT: ${button.textContent || button.innerText || 'N/A'}`);
});

// Trova CHECKBOX/RADIO
const checkboxes = document.querySelectorAll('input[type="checkbox"], input[type="radio"]');
console.log(`\n\nTrovati ${checkboxes.length} elementi CHECKBOX/RADIO:\n`);

checkboxes.forEach((cb, index) => {
    console.log(`\n--- CHECKBOX #${index + 1} ---`);
    console.log(`ID: ${cb.id || 'N/A'}`);
    console.log(`NAME: ${cb.name || 'N/A'}`);
    console.log(`VALUE: ${cb.value || 'N/A'}`);
    console.log(`TYPE: ${cb.type}`);
});

// Trova il FORM
const forms = document.querySelectorAll('form');
console.log(`\n\nTrovati ${forms.length} elementi FORM:\n`);

forms.forEach((form, index) => {
    console.log(`\n--- FORM #${index + 1} ---`);
    console.log(`ID: ${form.id || 'N/A'}`);
    console.log(`NAME: ${form.name || 'N/A'}`);
    console.log(`ACTION: ${form.action || 'N/A'}`);
    console.log(`METHOD: ${form.method || 'N/A'}`);
});

console.log("\n\n==========================================");
console.log("ANALISI COMPLETATA!");
console.log("==========================================");
console.log("\nCopia TUTTO l'output sopra e incollalo nella chat con Claude!");
