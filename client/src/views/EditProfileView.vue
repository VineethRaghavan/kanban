<template>
    <div class="vue-template vh-100 d-flex align-items-center" v-on:submit.prevent="onSubmit">
        <div class="card mx-auto d-flex" style="width: 18rem;">
            <h3 class="card-header">Edit profile</h3>
            <form class="form">
                <div class="form-group m-2">
                    <label>First name</label>
                    <input v-model="fname" type="text" class="form-control form-control-lg" />
                </div>
                <div class="form-group m-2">
                    <label>Last name</label>
                    <input v-model="lname" type="text" class="form-control form-control-lg" />
                </div>
                <div class="form-group m-2">
                    <label>Gender</label>
                    <input v-model="gender" type="text" class="form-control form-control-lg" />
                </div>
                <div class="form-group m-2">
                    <label>Date of birth</label>
                    <input v-model="birth_date" type="date" class="form-control form-control-lg" />
                </div>
                <div class="form-group m-2">
                    <label>Email address</label>
                    <input v-model="email" type="email" class="form-control form-control-lg" disabled/>
                </div>
                <div class="form-group m-2">
                    <label>Password</label>
                    <input v-model="password" type="password" class="form-control form-control-lg" />
                </div>
                <div class="form-group m-2">
                    <label>Confirm password</label>
                    <input v-model="confirm_password" type="password" class="form-control form-control-lg" />
                </div>
                <div class="form-group text-center">
                    <button :disabled="!isComplete" type="submit" class="btn btn-success btn-lg btn-block m-2">Save</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    name:"EditProfileView",
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
    async created(){
        this.fetchData()
    },
    methods:{
        async fetchData(){
            let token = sessionStorage.getItem("accessToken");
            let request = {
                url: "http://localhost:5000/get_profile",
                method: "get",
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    "Content-type": "application/json",
                    'Authorization': `Bearer ${token}`
                },
            };
            try {
                const response = await axios(request);
                console.log(response);
                this.fname = response.data.fname;
                this.lname = response.data.lname;
                this.gender = response.data.gender;
                this.birth_date = response.data.birth_date;
                this.email = response.data.email;
            } catch (error) {
                console.log(error)
                this.$router.push("/login");
            }
        },
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
                    url: "http://localhost:5000/update_profile",
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
                    alert("Profile updated successfully")
                    this.$router.push("/projects");
                } catch (error) {
                    alert(error.response.data.message)
                }
            }
        }
    }
}
</script>