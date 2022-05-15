<template>
  <div class="relative">
    <div class="container mt-6">
      <Button iconLeft="edit" :route="{ name: 'ProjectDetailUpdateNew' }">
        Write a new status update
      </Button>
      <div class="w-1/2 pr-4 mt-6 space-y-4">
        <div class="p-3 border rounded-lg" v-for="update in $resources.updates.data" :key="update.name">
          <UserInfo :email="update.owner" v-slot="{ user }">
            <div class="flex items-start space-x-2">
              <Avatar :label="user.full_name" :imageURL="user.user_image" />
              <div>
                <div class="flex items-center h-8 space-x-1">
                  <span class="text-base font-medium text-gray-900">
                    {{ user.full_name }}
                  </span>
                  <span> &middot; </span>
                  <Badge
                    :color="
                      {
                        'On Track': 'green',
                        'At Risk': 'orange',
                        'Off Track': 'red',
                      }[update.status]
                    "
                  >
                    {{ update.status }}
                  </Badge>
                  <span> &middot; </span>
                  <span
                    class="text-base text-gray-600"
                    :title="$dayjs(update.creation)"
                  >
                    {{ $dayjs(update.creation).fromNow() }}
                  </span>
                </div>
                <!-- <Badge
                  :color="
                    {
                      'On Track': 'green',
                      'At Risk': 'orange',
                      'Off Track': 'red',
                    }[update.status]
                  "
                >
                  Status: {{ update.status }}
                </Badge> -->
                <TextEditor :content="update.content" :editable="false" />
              </div>
            </div>
          </UserInfo>
        </div>
      </div>
    </div>
    <div
      class="absolute top-0 bottom-0 right-0 w-1/2 border-l"
      v-if="$route.name == 'ProjectDetailUpdateNew'"
    >
      <router-view :project="project" />
    </div>
  </div>
</template>
<script>
import { Avatar, TextEditor } from 'frappe-ui'

export default {
  name: 'ProjectDetailUpdate',
  props: ['project'],
  components: { TextEditor, Avatar },
  resources: {
    updates() {
      return {
        type: 'list',
        cache: ['Project Updates', this.project.doc.name],
        doctype: 'Team Project Status Update',
        filters: {
          project: this.project.doc.name,
        },
        fields: ['*'],
      }
    },
  },
}
</script>
