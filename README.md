# test_script

mongoose.connect(url, options).then( function() {
console.log('MongoDB is connected');
})
.catch( function(err) {
console.log(err);
});
 
const options = {
useNewUrlParser: true,
reconnectTries: Number.MAX_VALUE,
reconnectInterval: 500,
connectTimeoutMS: 10000,
};
