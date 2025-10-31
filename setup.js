console.log('🔧 1xBet GOOL Predictor Setup - Version 10.0');
console.log('🕒 ' + new Date().toISOString());
console.log('');

// Configuration check
const BOT_TOKEN = process.env.BOT_TOKEN || "YOUR_BOT_TOKEN_HERE";
const ADMIN_ID = process.env.ADMIN_ID || "6565594143";

console.log('🔍 CHECKING CONFIGURATION:');
console.log(BOT_TOKEN === "YOUR_BOT_TOKEN_HERE" ? '❌ BOT_TOKEN: NOT CONFIGURED' : '✅ BOT_TOKEN: CONFIGURED');
console.log(ADMIN_ID === "6565594143" ? '⚠️ ADMIN_ID: USING DEFAULT' : '✅ ADMIN_ID: CONFIGURED');

console.log('');
console.log('📦 CHECKING DEPENDENCIES:');

const deps = ['telegraf', 'axios', 'cheerio', 'node-cron', 'dotenv', 'moment'];
deps.forEach(dep => {
    try {
        require(dep);
        console.log(`✅ ${dep}: INSTALLED`);
    } catch {
        console.log(`❌ ${dep}: MISSING`);
    }
});

console.log('');
console.log('🎯 BOT FEATURES:');
console.log('✅ 1xBet Account Verification');
console.log('✅ GOOL Predictions (Goal/No Goal)');
console.log('✅ AI Analysis Engine');
console.log('✅ Live Updates');
console.log('✅ Arabic Interface');
console.log('✅ Working Buttons');
console.log('✅ User Statistics');
console.log('✅ Real-time Data');

console.log('');
console.log('🚀 STARTING BOT...');
console.log('');

setTimeout(() => {
    require('./bot.js');
}, 2000);