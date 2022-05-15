<template>
  <div class="container mt-6">
    <div class="grid grid-cols-6 gap-6">
      <ProjectDetailOverviewReadme
        class="col-span-4 border"
        :project="project"
      />
      <ProjectDetailOverviewStatusUpdate
        class="col-span-2"
        :project="project"
      />
    </div>
    <!-- <ProjectDetailOverviewMembers class="w-1/2" :project="project" /> -->
    <!-- <ProjectDetailOverviewLinks class="w-1/2" :project="project" /> -->
  </div>
</template>
<script>
import ProjectDetailOverviewMembers from './ProjectDetailOverviewMembers.vue'
import ProjectDetailOverviewLinks from './ProjectDetailOverviewLinks.vue'
import ProjectDetailOverviewStatusUpdate from './ProjectDetailOverviewStatusUpdate.vue'
import ProjectDetailOverviewReadme from './ProjectDetailOverviewReadme.vue'

export default {
  name: 'ProjectDetailOverview',
  props: ['project'],
  components: {
    ProjectDetailOverviewLinks,
    ProjectDetailOverviewStatusUpdate,
    ProjectDetailOverviewMembers,
    ProjectDetailOverviewReadme,
  },
}
</script>
