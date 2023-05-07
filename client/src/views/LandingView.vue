<template>
    <div class="mx-auto d-flex justify-content-between border-bottom">
        <h3 class="m-3">Kanban application</h3>
    </div>
    <div class="vue-template d-flex align-items-center" v-on:submit.prevent="onSubmit">
        <div class="card mx-auto m-4" style="width: 50rem;">
            <h3 class="card-header">Project details</h3>
            <div class="card-body overflow-auto">
                <div class="container">
                    <ul class="list-group list-group-flush">
                        <div class="row">
                            <div class="col-md-6">
                                <li class="list-group-item">
                                    <div class="mx-auto d-flex justify-content-between align-items-center text-muted">
                                        Made by: 
                                    </div>
                                    <h4>Vineeth Raghavan</h4>
                                </li>
                                <li class="list-group-item">
                                    <div class="mx-auto d-flex justify-content-between align-items-center text-muted">
                                        Under the guidance of:
                                    </div>
                                    <h4>Dr. Samyama Gunjal G. H.</h4>
                                </li>
                                <li class="list-group-item">
                                    <div class="mx-auto d-flex justify-content-between align-items-center text-muted">
                                        Tools used:
                                    </div>
                                    <p>
                                        Python and Flask framework for the backend.<br>
                                        Javascript and VueJS library for the frontend.<br>
                                        SQLite for database.
                                    </p>
                                </li>
                            </div>
                            <div class="col-md-6">
                                
                                <li class="list-group-item">
                                    <div class="mx-auto d-flex justify-content-between align-items-center text-muted">
                                        Description:
                                    </div>
                                    <p>
                                        Kanban methodology is a workflow methodology that is used to make working in teams more efficient. Kanban applications help achieve this by creating a Kanban board which lists tasks that have to be completed. The tasks can be organized on the basis of status, i.e. "Pending", "In progress", or "Completed". The users can further add more status types to be more specific. This board is visible to all users and it can help them get a bird’s eye view of the tasks and their status.
                                    </p>
                                </li>
                            </div>
                        </div>
                    </ul>
                </div>  
            </div>
            <div class="m-4 text-center">
                <router-link to="/register" class="btn btn-primary">Proceed to application</router-link>
            </div>
        </div>
    </div>
</template>

<script>

export default{
    name:"LandingView",
}
</script>