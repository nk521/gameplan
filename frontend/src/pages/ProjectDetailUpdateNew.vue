<template>
  <div class="p-6">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-semibold text-gray-900">New Project Update</h2>
      <div class="space-x-2">
        <Button
          appearance="primary"
          :loading="$resources.newUpdate.loading"
          @click="$resources.newUpdate.submit({ content, status })"
        >
          Publish
        </Button>
        <Button :route="{ name: 'ProjectDetailUpdate' }">Discard</Button>
      </div>
    </div>
    <div class="mt-3 space-x-2">
      <Button
        :appearance="d.name === status ? d.appearance : 'secondary'"
        v-for="d in statuses"
        :key="d.name"
        @click="status = d.name"
      >
        <span :class="d.name !== status ? d.textColor : null">
          {{ d.name }}
        </span>
      </Button>
    </div>
    <TextEditor
      class="mt-3"
      editor-class="px-3 py-2 border rounded-b-lg max-w-[unset] min-h-[20rem]"
      :content="content"
      @change="(val) => (content = val)"
      :bubbleMenu="true"
      :fixedMenu="true"
    />
  </div>
</template>
<script>
import { Avatar, TextEditor } from 'frappe-ui'

export default {
  name: 'ProjectDetailUpdateNew',
  props: ['project'],
  components: { TextEditor, Avatar },
  data() {
    return {
      status: '',
      content: `
        <h3>What we've accomplished</h3>
        <p></p>
        <h3>What's blocked</h3>
        <p></p>
        <h3>Next Steps</h3>
        <p></p>
      `,
    }
  },
  resources: {
    newUpdate() {
      return {
        method: 'frappe.client.insert',
        makeParams({ content, status }) {
          return {
            doc: {
              doctype: 'Team Project Status Update',
              project: this.project.doc.name,
              content,
              status,
            },
          }
        },
        validate(params) {
          if (!params.doc.status) {
            return `Please select project status before publishing.`
          }
        },
        onSuccess() {
          this.$router.replace({ name: 'ProjectDetailUpdate' })
          this.$getListResource([
            'Project Updates',
            this.project.doc.name,
          ]).reload()
          this.status = null
          this.content = ''
        },
        onError(e) {
          let message = e.messages ? e.messages.join('\n') : e.message
          this.$toast({
            title: 'Project Update Error',
            text: message,
            icon: 'alert-circle',
            iconClasses: 'text-red-600',
          })
        },
      }
    },
  },
  computed: {
    statuses() {
      return [
        {
          name: 'On Track',
          textColor: 'text-green-600',
          appearance: 'success',
        },
        {
          name: 'At Risk',
          textColor: 'text-yellow-600',
          appearance: 'warning',
        },
        { name: 'Off Track', textColor: 'text-red-600', appearance: 'danger' },
      ]
    },
  },
}
</script>
