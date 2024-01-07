<template>
  <div class="main-container">
    <div>
      <p>
        Go to characters page:
        <router-link to="/characters">Characters</router-link>
      </p>
      <h1>World</h1>
      <h2>Character</h2>
      <p>
        Name: {{ characterName }} Gender: {{ character.gender }} Alive:
        {{ character.alive }} Level: {{ character.level }} XP:
        {{ character.xp }} Money: {{ character.money }} Class:
        {{ character.base_class.name }} ID: {{ character.id }}
      </p>
      <WorldMap data-test="enterWorld" :player="character" :height="500" :width="500" :scale="scale" @moveUp="moveUp"
        @moveDown="moveDown" @moveLeft="moveLeft" @moveRight="moveRight" @playerUpdated="handlePlayerUpdate" />
    </div>
    <div>
      <Chat :player="character" />
    </div>
  </div>
</template>

<script setup>
import { get, update } from "~/requests";
import { useCharacterStore } from "~/store/character";

const characterStore = useCharacterStore();
const { getCharacter } = characterStore;
const character = ref(getCharacter());

const places = ref([]);
const scale = 10;

const characterName = computed(() => character.value.character_name);

const moveUp = async () => {
  await update(`/character-locations/${character.value.id}`, {
    y: character.value.character_location.y,
  });
};
const moveDown = async () => {
  await update(`/character-locations/${character.value.id}`, {
    y: character.value.character_location.y,
  });
};
const moveLeft = async () => {
  await update(`/character-locations/${character.value.id}`, {
    x: character.value.character_location.x,
  });
};
const moveRight = async () => {
  await update(`/character-locations/${character.value.id}`, {
    x: character.value.character_location.x,
  });
};

const handlePlayerUpdate = updatedPlayer => {
  character.value = updatedPlayer;
};
</script>

<style>
.main-container {
  display: flex;

}
</style>