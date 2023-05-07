<template>
    <div class="vue-template vh-100 d-flex align-items-center" v-on:submit.prevent="onSubmit">
        <div class="card mx-auto" style="width: 18rem;">
            <h3 class="card-header">Sign In</h3>
            <form class="form">
                <div class="form-group m-2">
                    <label>Email address</label>
                    <input v-model="email" type="email" class="form-control form-control-lg">
                </div>
                <div class="form-group m-2">
                    <label>Password</label>
                    <input v-model="password" type="password" class="form-control form-control-lg">
                </div>
                <div class="form-group text-center">
                    <button :disabled='!isComplete' type="submit" class="btn btn-success btn-lg btn-block m-2">Sign In</button>
                </div>
            </form>
            <div class="my-4">
                <p class="mb-0 text-center">Don't have an account? <router-link to="/register" class="text-black-50 text-decoration-none">Sign Up</router-link></p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    name:"LoginView",
    data(){
        return{
            email:'',
            password:''
        }
    },
    computed: {
        isComplete(){
            return this.email && this.password
        }
    },
    methods:{
        async onSubmit(){
            let data = {
                email: this.email, 
                password: this.password
            };

            let request = {
                url: "http://localhost:5000/login",
                method: "post",
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    "Content-type": "application/json"
                },
                data: JSON.stringify(data)
            };
            try {
                const response = await axios(request);
                sessionStorage.setItem("accessToken", response.data.access_token)
                this.$router.push("/projects")
            } catch (error) {
                alert(error.response.data)
            }
            
        }
    }
}
</script>