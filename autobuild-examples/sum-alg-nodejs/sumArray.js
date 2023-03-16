module.exports.start = args =>{
    return args.input[0].reduce((x,y) => x+y);
}