<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template >
<div>
  <header>

    <div >
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</div>

</template>

