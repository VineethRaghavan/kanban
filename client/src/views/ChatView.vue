<template>
    <div class="vue-template vh-100 d-flex align-items-center" v-on:submit.prevent="onSubmit">
        <div class="card mx-auto d-flex" style="width: 50rem; height: 40rem">
            <h3 class="card-header">Chat</h3>
            <div class="card-body overflow-auto" style="height: 15rem">
                    <ul class="list-group list-group-flush ">
                        <li class="list-group-item" v-for="chat in chats" :key="chat.chat_id">
                            <div class="mx-auto d-flex justify-content-between align-items-center text-muted">
                                <div>{{ chat.email }}</div>
                                <div>{{ chat.date_time }}</div>
                            </div>
                            <div>{{ chat.text }}</div>
                        </li>
                    </ul>
                </div>
            <form class="form">
                <div class="form-group m-2">
                    <input v-model="text" type="text" placeholder="Text Message" class="form-control form-control-lg" />
                </div>
                <div class="form-group text-center">
                    <button :disabled="!isComplete" type="submit" class="btn btn-success btn-lg btn-block m-2">Send</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    name:"ChatView",
    data(){
        return{
            text: '',
            chats:null
        }
    },
    computed:{
        isComplete(){
            return this.text != ''
        }
    },
    async created(){
        this.fetchData()
    },
    methods:{
        async fetchData(){
            let token = sessionStorage.getItem("accessToken");
            let request = {
                url: "http://localhost:5000/chat_messages",
                params:{ project_id: this.$route.query.project },
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
                this.chats = response.data;
            } catch (error) {
                console.log(error)
                this.$router.push("/login");
            }
        },
        async onSubmit(){
            let token = sessionStorage.getItem("accessToken");
            let data = {
                text: this.text,
                date_time: new Date().toLocaleString('en-GB'),
                project_id: this.$route.query.project
            };

            let request = {
                url: "http://localhost:5000/add_chatmessage",
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
                this.fetchData()
                this.text = ''
            } catch (error) {
                alert(error.response.data.message)
            }
        }
    }
}
</script>