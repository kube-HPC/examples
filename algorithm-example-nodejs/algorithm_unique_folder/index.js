const vm = require('vm');

const start = async (payload) => {
    console.log(`algorithm: start`);
    const { input, info } = payload;
    const codeInfo = info && info.extraData && info.extraData.code;
    const code = codeInfo && codeInfo.join && codeInfo.join('\n');

    if (code) {
        const result = await runCode(code, input);
        return result;
    }
    return input[0];
}

const runCode = (code, input) => {
    return new Promise(async (resolve, reject) => {
        try {
            const result = await vm.runInThisContext(`(${code})`)(input);
            return resolve(result);
        }
        catch (error) {
            return reject(error);
        }
    });
}

module.exports = {
    start
}
