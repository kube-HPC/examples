module.exports.start = (args) => {
    console.log('algorithm: reduce start');
    const input = args.input[0];
    return input.reduce((accum, curValue) => accum + curValue);
}
