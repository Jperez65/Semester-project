const vm = new Vue({ // Again, vm is our Vue instance's name for consistency.
    el: '#vm',
    delimiters: ['[[', ']]'],
    data: {
        username:'',
        password: '',
    },
    methods: {
        logToConsole () {
            alert('email' + this.email);
        }
        

    }
})