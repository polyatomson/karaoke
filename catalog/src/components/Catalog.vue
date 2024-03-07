<template>
    <div class="flex justify-content-center">
        <!-- <Button label="Reload" @click="getCatalog"/> -->
        <Dropdown v-if="mobile" v-model="selectedOrigin" :options="origins" />
    </div>
    <Card style="margin: auto; margin-top: 1rem;" class="pd-card" :pt="{header: {class: 'bg-primary'}, content: {class: 'text-sm'}}">
        <template #header>
            <div style="height: 1rem;"></div>
        </template>
        <template #content>
            <DataTable :value="songsFromOrigin" size="small" scrollable :scrollHeight="scrollH"
            sortMode="multiple" v-model:filters="filters" 
            removableSort
            filterDisplay="row"
            :globalFilterFields="['artist', 'title']"
            >

            <template #header>
                <div class="flex justify-content-end">
                    <IconField>
                    <InputIcon class="pi pi-search"> </InputIcon>
                        <InputText v-model="filters['global'].value" placeholder="Keyword Search" />
                    </IconField>
                </div>
            </template>
                <Column field="liked" sortable style="max-width: 4rem;" frozen alignFrozen="left">
                    <template #body="{ data }">
                        <Button :icon="favoriteFill(data)" size="small" severity="error" @click="Like(data)"/>
                    </template>
                </Column>

                <Column v-if="!mobile" field="origin" 
                :showFilterMenu="false"
                 style="max-width: 4rem;" header="Lang" sortable
                 
                  >
                    <template #body="{ data, field }">
                        <Tag :value="data[field]" :severity="getColor(data[field])" />
                    </template>
                    <template #filter="{ filterModel, filterCallback }">
                        <Dropdown v-model="filterModel.value" 
                        @change="filterCallback()"
                        :options="origins"
                        class="" style="min-width: 3rem"
                        />
                    </template>
                </Column>
                <Column field="artist" style="max-width: 8rem;" :pt="{body: {class: 'flex flex-wrap'}}" header="Artist" sortable>
                    <template v-if="!mobile" #filter="{ filterModel, filterCallback }">
                        <InputText v-model="filterModel.value" type="text" @input="filterCallback()" class="p-column-filter" placeholder="Search" />
                    </template>
                </Column>
                <Column field="title" style="max-width: 8rem" :pt="{body: {class: 'flex flex-wrap'}}" header="Title" sortable>
                    <template v-if="!mobile" #filter="{ filterModel, filterCallback }">
                        <InputText v-model="filterModel.value" type="text" @input="filterCallback()" class="p-column-filter" placeholder="Search" />
                    </template>
                </Column>
                <Column v-if="!mobile" field="vocals" style="max-width: 10%" header="Voice" sortable>
                    <template #body="{ data, field}">
                        <i v-if="data[field]===1" class="pi pi-check" style="font-size: 1rem"></i>
                        <i v-if="data[field]===0" class="pi pi-times" style="font-size: 1rem"></i>
                        </template>
                </Column>
                <Column field="link" style="max-width: 10rem;" frozen alignFrozen="right" header="Link">
                <template #body="{ data, field }">
                <a :href="'https://www.youtube.com/watch?v='+data[field]" target="_blank" rel="noopener noreferrer">
                    <Button v-if="mobile" icon="pi pi-external-link" size="small" :severity="visitedColor(data)" @click="addView(data.song_id)"/>
                    <Button v-else label="Open" class="text-sm" icon="pi pi-external-link" size="small" :severity="visitedColor(data)" @click="addView(data.song_id)"/>
                </a>
                </template>
                </Column>
            </DataTable>
        </template>
    </Card>
</template>
<script setup>
import { onBeforeMount, onBeforeUnmount, onBeforeUpdate, onMounted, ref, watch } from 'vue'
import { FilterMatchMode } from 'primevue/api';

const songs = ref()
const viewed = ref()
const mobile = ref()
const scrollH = ref()

const favs = ref()



const favoriteFill = (data) => {
    if (favs.value.includes(data.song_id)) {
        data.liked = 0
        return 'pi pi-heart-fill'
    }
    else {
        data.liked = 1
        return 'pi pi-heart'
    }
}

const Like = (data) => {
    const song_id = data.song_id
    if (favs.value.includes(song_id)) {
        favs.value = favs.value.filter((id) => id !== song_id)
        data.liked = 1
    }
    else {
        favs.value.push(song_id)
        data.liked = 0
    }
}

const visitedColor = (data) => {
    if (viewed.value.includes(data.song_id)) {
        return 'warning'
    }
    else {
        return 'info'
    }
}

const origins = ref()
const selectedOrigin = ref('SLO')
const songsFromOrigin = ref()



const filters = ref({
                artist: { value: null, matchMode: FilterMatchMode.CONTAINS },
                title: { value: null, matchMode: FilterMatchMode.CONTAINS },
                origin: { value: null, matchMode: FilterMatchMode.EQUALS },
                global: { value: null, matchMode: FilterMatchMode.CONTAINS }
            })


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
        case 'EN':
            return 'warning';

        case 'SLO':
            return 'success';

        case 'EX-YU':
            return 'info';
        
        default: 
            return 'danger'
    }
}


async function getCatalog() {
    console.log('making GET query')
    const response = await fetch(
        import.meta.env.VITE_APP_API_URL + '/catalog', 
          {
            mode: 'cors',
            method: 'GET',
            headers: {
              "Content-Type": "application/json"
            }
          })
    const received = await response.json();
    songs.value = received.songs;
    origins.value = received.origins;
    console.log('songs recieved, example:', received.songs[0])
}

async function addView(song_id) {
    console.log('adding view for', song_id)
    const response = await fetch(
        import.meta.env.VITE_APP_API_URL+'/view', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({song_id})
          })
    const reply = await response.text();
    console.log(reply)

    viewed.value.push(song_id)
    
}

const detectMob = () => {
    console.log(window.innerWidth)
    return ( ( window.innerWidth <= 500 ) );
  }

onBeforeMount(() => {
    const windHeight = window.innerHeight
    scrollH.value = windHeight.toString() + 'px'
    console.log(scrollH.value)
    
    const favourites = localStorage.getItem('favourites')
    console.log('favorites', favourites)
    if (favourites != 'undefined' && favourites != null) {
        favs.value = JSON.parse(favourites)

    }
    else {
        favs.value = []
    }
    const visited = localStorage.getItem('visited')
    console.log('visited', visited)
    if (visited != 'undefined' && visited != null) {
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


window.addEventListener('beforeunload', (event) => {
        // Cancel the event as stated by the standard.
        // event.preventDefault();
        console.log('before leaving', viewed.value)
        localStorage.setItem('visited', JSON.stringify(viewed.value))
        localStorage.setItem('favourites', JSON.stringify(favs.value))
        // Chrome requires returnValue to be set.
        event.returnValue = '';
      });

</script>