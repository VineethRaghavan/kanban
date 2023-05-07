<template>
    <div class="vue-template vh-100 d-flex align-items-center" v-on:submit.prevent="onSubmit">
        <div class="card mx-auto d-flex" style="width: 30rem;">
            <h3 class="card-header">Sign Up</h3>
            <form class="form">
                <div class="container">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group m-1">
                                <label>First name</label>
                                <input v-model="fname" type="text" class="form-control form-control-lg" />
                            </div>
                            <div class="form-group m-1">
                                <label>Last name</label>
                                <input v-model="lname" type="text" class="form-control form-control-lg" />
                            </div>
                            <div class="form-group m-1">
                                <label>Gender</label>
                                <input v-model="gender" type="text" class="form-control form-control-lg" />
                            </div>
                            <div class="form-group m-1">
                                <label>Date of birth</label>
                                <input v-model="birth_date" type="date" class="form-control form-control-lg" />
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-group m-1">
                                <label>Email address</label>
                                <input v-model="email" type="email" class="form-control form-control-lg" />
                            </div>
                            <div class="form-group m-1">
                                <label>Password</label>
                                <input v-model="password" type="password" class="form-control form-control-lg" />
                            </div>
                            <div class="form-group m-1">
                                <label>Confirm password</label>
                                <input v-model="confirm_password" type="password" class="form-control form-control-lg" />
                            </div>
                        </div>
                    </div>
                    <div class="form-group text-center">
                        <button :disabled="!isComplete" type="submit" class="btn btn-success btn-lg btn-block m-2">Sign Up</button>
                    </div>
                </div>
            </form>
            <div class="my-4">
                <p class="mb-0 text-center">Already have an account? <router-link to="/login" class="text-black-50 text-decoration-none">Sign In</router-link></p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    name:"RegisterView",
    data(){
        return{
            fname: '',
            lname: '',
            gender: '',
            birth_date: '',
            email: '',
            password: '',
            confirm_password: ''
        }
    },
    computed:{
        isComplete(){
            return this.fname && this.lname && this.gender && this.birth_date && this.email && this.password && this.confirm_password
        }
    },
    methods:{
        async onSubmit(){
            if(this.confirm_password != this.password)
                alert("Passwords don't match")
            else {
                let data = {
                    fname: this.fname,
                    lname: this.lname,
                    gender: this.gender,
                    birth_date: this.birth_date,
                    email: this.email,
                    password: this.password
                };

                let request = {
                    url: "http://localhost:5000/register",
                    method: "post",
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        "Content-type": "application/json"
                    },
                    data: JSON.stringify(data)
                };
                try {
                    const response = await axios(request);
                    console.log(response);
                    alert("Registration successful")
                    this.$router.push("/login");
                } catch (error) {
                    alert(error.response.data.message)
                }
            }
        }
    }
}
</script>