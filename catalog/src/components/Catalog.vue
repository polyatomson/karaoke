<template>
    <div class="flex justify-content-center">
        <Button label="Reload" @click="getCatalog"/>
    </div>
    <Card style="margin: auto; margin-top: 1rem;" class="pd-card" :pt="{header: {class: 'bg-primary'}, content: {class: 'text-sm'}}">
        <template #header>
            <div style="height: 1rem;"></div>
        </template>
        <template #content>
            <DataTable :value="songs" size="small" scrollable scrollHeight="300rem">
                <Column field="origin" header="Origin">
                    <template #body="{ data, field }">
                        <Tag :value="data[field]" :severity="getColor(data[field])" />
                    </template>
                </Column>
                <Column field="artist" style="max-width: 5rem;" :pt="{body: {class: 'flex flex-wrap'}}" header="Artist"></Column>
                <Column field="title" style="max-width: 5rem;" :pt="{body: {class: 'flex flex-wrap'}}" header="Title"></Column>
                <Column field="link" header="Link">
                <template #body="{ data, field }">
                <a :href="data[field]" target="_blank">
                    <Button v-if="!viewed.includes(data.song_id)" label="Open" class="text-sm" size="small" severity="info" @click="addView(data.song_id)"/>
                    <Button v-else="viewed.includes(data.song_id)" label="Repeat" class="text-sm" size="small" severity="warning" @click="addView(data.song_id)"/>
                </a>
                </template>
                </Column>
                <Column field="vocals" header="Voice">
                    <template #body="{ data, field}">
                        <i v-if="data[field]===1" class="pi pi-check" style="font-size: 1rem"></i>
                        <i v-if="data[field]===0" class="pi pi-times" style="font-size: 1rem"></i>
                        </template>
                </Column>
            </DataTable>
        </template>
    </Card>
</template>
<script setup>
import { onMounted, ref } from 'vue'
const songs = ref()
const viewed = ref([])

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
}

async function addView(song_id) {
    console.log('adding view for', song_id)
    const response = await fetch(
          'http://localhost:7000/view', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'song_id': song_id})
          })
    const reply = await response.text();
    console.log(reply)

    viewed.value.push(song_id)
    
}

onMounted(async () => {
    getCatalog()
}
)
</script>