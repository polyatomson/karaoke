<template>
    <div class="flex justify-content-center">
        <Button label="Reload" @click="getCatalog"/>
    </div>
    <Card style="margin: auto; margin-top: 1rem;" class="pd-card" :pt="{header: {class: 'bg-primary'}}">
        <template #header>
            <div style="height: 1rem;"></div>
        </template>
        <template #content>
            <DataTable :value="songs">
                <Column field="origin" header="Origin">
                    <template #body="{ data, field }">
                        <Tag :value="data[field]" :severity="getColor(data[field])" />
                    </template>
                </Column>
                <Column field="artist" header="Artist"></Column>
                <Column field="title" header="Title"></Column>
                <Column field="vocals" header="Voice">
                    <template #body="{ data, field}">
                        <i v-if="data[field]===1" class="pi pi-check" style="font-size: 1rem"></i>
                        <i v-if="data[field]===0" class="pi pi-times" style="font-size: 1rem"></i>
                        </template>
                </Column>
                <Column field="link" header="Link">
                <template #body="{ data, field }">
                
                </template>
                </Column>
            </DataTable>
        </template>
    </Card>
</template>
<script setup>
import { onMounted, ref } from 'vue'
const songs = ref() 

const getColor = (origin) => {
    switch (origin) {
        case 'Forein':
            return 'danger';

        case 'SLO':
            return 'success';

        case 'EX-YU':
            return 'info';

        case 'RU':
            return 'warning';
    }
}


async function getCatalog() {
    console.log('making GET query')
    const response = await fetch(
          'http://localhost:7000/catalog', 
          {
            mode: 'cors',
            method: 'GET',
            headers: {
              "Content-Type": "application/json"
            }
          })
    const received = await response.json();
    songs.value = received.songs;
    console.log('songs recieved, example:', received.songs[0])
    localStorage.setItem("songs", JSON.stringify(received.songs));
}
onMounted(async () => {
    const loadedSongs = localStorage.getItem('songs')
    if (loadedSongs === null) {
        getCatalog()
    }
    else {
        console.log('already in storage')
        songs.value = JSON.parse(loadedSongs)
    }
}
)
</script>