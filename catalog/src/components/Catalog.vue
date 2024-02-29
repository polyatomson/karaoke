<template>
    <div class="flex justify-content-center">
        <!-- <Button label="Reload" @click="getCatalog"/> -->
        <SelectButton v-if="mobile" v-model="selectedOrigin" :options="origins"/>
    </div>
    <Card style="margin: auto; margin-top: 1rem;" class="pd-card" :pt="{header: {class: 'bg-primary'}, content: {class: 'text-sm'}}">
        <template #header>
            <div style="height: 1rem;"></div>
        </template>
        <template #content>
            <DataTable :value="songsFromOrigin" size="small" scrollable :scrollHeight="scrollH">
                <Column v-if="!mobile" field="origin" style="max-width: 10rem;" header="Origin">
                    <template #body="{ data, field }">
                        <Tag :value="data[field]" :severity="getColor(data[field])" />
                    </template>
                </Column>
                <Column field="artist" style="max-width: 8rem;" :pt="{body: {class: 'flex flex-wrap'}}" header="Artist"></Column>
                <Column field="title" style="max-width: 8rem" :pt="{body: {class: 'flex flex-wrap'}}" header="Title"></Column>
                <Column v-if="!mobile" field="vocals" style="max-width: 10%" header="Voice">
                    <template #body="{ data, field}">
                        <i v-if="data[field]===1" class="pi pi-check" style="font-size: 1rem"></i>
                        <i v-if="data[field]===0" class="pi pi-times" style="font-size: 1rem"></i>
                        </template>
                </Column>
                <Column field="link" style="max-width: 10rem;" frozen alignFrozen="right" header="Link">
                <template #body="{ data, field }">
                <a :href="data[field]" target="_blank" rel="noopener noreferrer">
                    <Button v-if="!viewed.includes(data.song_id)" label="Open" class="text-sm" size="small" severity="info" @click="addView(data.song_id)"/>
                    <Button v-else="viewed.includes(data.song_id)" label="Repeat" class="text-sm" size="small" severity="warning" @click="addView(data.song_id)"/>
                </a>
                </template>
                </Column>
            </DataTable>
        </template>
    </Card>
</template>
<script setup>
import { onBeforeMount, onBeforeUnmount, onBeforeUpdate, onMounted, ref, watch } from 'vue'
const songs = ref()
const viewed = ref()
const mobile = ref()
const scrollH = ref()

const origins = ref(['SLO', 'EX-YU', 'Foreign'])
const selectedOrigin = ref('SLO')
const songsFromOrigin = ref()

watch(selectedOrigin, async(newOrigin) => {
    console.log('watch works', newOrigin)
    pickOrigin(selectedOrigin.value)
}
)


const pickOrigin = (pickedOrigin) => {
    songsFromOrigin.value = songs.value.filter(song => song.origin === pickedOrigin)
}

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

const detectMob = () => {
    return ( ( window.outerWidth <= 500 ) );
  }

onBeforeMount(() => {
    const windHeight = window.innerHeight
    scrollH.value = windHeight.toString() + 'px'
    console.log(scrollH.value)
    const visited = localStorage.getItem('visited')
    console.log('visited', visited, typeof(visited))
    if (visited != 'undefined') {
        viewed.value = JSON.parse(visited)
    }
    else {
        viewed.value = []
    }
    console.log(viewed.value)
    console.log(scrollH.value)
})

onMounted(async () => {
    getCatalog().then( () => {
    if (detectMob()) {
        mobile.value = true
        pickOrigin('SLO')
    }
    else {
        mobile.value = false
        songsFromOrigin.value = songs.value
    }
})
}
)

// onBeforeUnmount(() => {
//     console.log('before update', viewed.value)
//     localStorage.setItem('visited', JSON.stringify(viewed.value))
// })

window.addEventListener('beforeunload', (event) => {
        // Cancel the event as stated by the standard.
        // event.preventDefault();
        console.log('before leaving', viewed.value)
        localStorage.setItem('visited', JSON.stringify(viewed.value))
        // Chrome requires returnValue to be set.
        event.returnValue = '';
      });

</script>