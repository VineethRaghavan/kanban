<template>
    <div class="mx-auto d-flex justify-content-between border-bottom">
        <h3 class="m-3">Projects</h3>
        <button type="button" @click="addProject" class="btn btn-success btn-block m-3">Add new project</button>
        <button type="button" @click="manageStatuses" class="btn btn-primary btn-block m-3">Manage statuses</button>
        <button type="button" @click="onSearch" class="btn btn-warning btn-block m-3">Search</button>
        <button type="button" @click="editProfile" class="btn btn-outline-primary btn-block m-3">Edit profile</button>
        <button type="button" @click="logOut" class="btn btn-outline-secondary btn-block m-3">Log out</button>
    </div>
    <div class="vue-template vh-100 d-flex flex-wrap">
        <div v-for="project in projects" :key="project.project_id" class="card mx-auto m-3" style="width: 14rem; height: 12rem;">
            <router-link :to="{ path: '/tasks', query: { project: project.project_id }}" class="text-black text-decoration-none">
                <h5 class="card-title text-center card-header">{{ project.name }}</h5>
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">Start date: {{ project.start_date }}</li>
                    <li class="list-group-item">End date: {{ project.end_date }}</li>
                </ul>
            </router-link>
            <button type="button" @click="deleteProject(project.project_id)" class="btn btn-danger btn-block m-3">Delete</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    name:"ProjectsView",
    data(){
        return{
            projects: null
        }
    },

    async created(){
        this.fetchData();
    },
    methods:{
        logOut(){
            sessionStorage.clear();
            this.$router.push("/login");
        },
        editProfile(){
            this.$router.push("/edit_profile");
        },
        addProject(){
            this.$router.push("/add_project")
        },
        manageStatuses(){
            this.$router.push("/manage_statuses")
        },
        onSearch(){
            this.$router.push("/search")
        },
        async deleteProject(project_id){
            if(confirm("Are you sure you want to delete this project?")){
                let token = sessionStorage.getItem("accessToken")
                let data = {
                    project_id: project_id
                };

                let request = {
                    url: "http://localhost:5000/delete_project",
                    method: "post",
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        "Content-type": "application/json",
                        'Authorization': `Bearer ${token}`
                    },
                    data: JSON.stringify(data)
                };
                try {
                    const response = await axios(request);
                    console.log(response);
                    this.fetchData();
                    alert("Project deleted successfully");
                } catch (error) {
                    console.log(error)
                    alert(error.response.data.message)
                }
            }
        },
        async fetchData(){
            let token = sessionStorage.getItem("accessToken");
            let request = {
                url: "http://localhost:5000/projects",
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
                this.projects = response.data;
            } catch (error) {
                console.log(error)
                this.$router.push("/login");
            }
        }
    }
}
</script>