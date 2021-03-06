/** * Dashboard of app */

<template>
  <v-container>
    <v-row class="ma-2">
      <v-col cols="12" v-if="isAdmin">
        <VirtualCardCount />
      </v-col>
      <!-- <v-col cols="12">  -->
      <v-col cols="12">
        <v-card class="mx-auto">
          <v-toolbar flat class="bc-subtitle" dark>
            <h1 class="bc-h1-sub-ttile">{{ $t('dashboard.pagetitle') }}</h1>
            <div class="flex-grow-1"></div>
          </v-toolbar>
          <v-divider></v-divider>
          <v-container>
            <v-row class="ma-2">
              <v-col cols="12">
                <v-card-subtitle
                  class="text-left bc-padding-left-0 page-info pa-2"
                  v-html="$t('dashboard.createProjectInfo')"
                ></v-card-subtitle>
                <!-- </v-col> -->
                <Button
                  class="white--text ml-3 yellow-btn"
                  depressed
                  :yellowBtn="true"
                  @click="$router.push(`/project/info`)"
                  @keyup.enter="$router.push(`/project/info`)"
                  name="btn-create-project"
                  data-test-id="btn-create-project"
                  :aria-label="$t('dashboard.areaLabelbtnCreateProject')"
                >{{ $t('dashboard.btnCreateProject') }}</Button>
                <v-col cols="12" md="12" v-if="projectInfoList.length > 0">
                  <h2 class="bc-page-title-h1 px-2 mb-2">{{ $t('dashboard.myprojectTitle') }}</h2>

                  <v-simple-table class="text-left">
                    <template v-slot:default>
                      <thead class="table-head">
                        <tr>
                          <th
                            :scope="$t('dashboard.tblTitleProjectName')"
                          >{{ $t('dashboard.tblTitleProjectName') }}</th>
                          <th
                            :scope="$t('dashboard.tblTitleReferenceNo')"
                          >{{ $t('dashboard.tblTitleReferenceNo') }}</th>
                          <th
                            :scope="$t('dashboard.tblTitlCreated')"
                          >{{ $t('dashboard.tblTitlCreated') }}</th>
                          <th
                            :scope="$t('dashboard.tblTitlrole')"
                            v-if="isClient"
                          >{{ $t('dashboard.tblTitlrole') }}</th>
                          <th
                            :scope="$t('dashboard.tblTitleProjectStatus')"
                          >{{ $t('dashboard.tblTitleProjectStatus') }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="project in projectInfoList"
                          :key="project.id"
                          @click="redirectToProject(project)"
                          @keyup.enter="redirectToProject(project)"
                          style="cursor: pointer"
                          tabindex="0"
                        >
                          <td>{{ project.name }}</td>
                          <td>{{ project.id }}</td>
                          <td>{{ project.created }}</td>
                          <td v-if="isClient">
                            {{
                            $t(
                            project.role &&
                            `projectRoles.role${
                            projectRolesList[project.role]
                            }`
                            )
                            }}
                          </td>

                          <td>
                            <div class="bc_project_status" :class="getStatusClass(project.status)"></div>
                            {{
                            $t(
                            `projectStatus.status${
                            projectStatusList[project.status]
                            }`
                            )
                            }}
                          </td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </v-col>
                <v-col cols="12" md="12" v-else>
                  <v-card flat class="text-left">
                    <v-card-text>{{ $t('dashboard.noData') }}</v-card-text>
                  </v-card>
                </v-col>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { Getter, namespace, Action } from 'vuex-class';
import { projectStatus, projectRoles } from '@/constants/enums';
import VirtualCardCount from '@/components/Dashboard/VirtualCardCount.vue';

import Button from '@/Atomic/Button/Button.vue';

const ProjectInfoModule = namespace('ProjectInfoModule');
const KeyCloakModule = namespace('KeyCloakModule');
const SharedModule = namespace('SharedModule');

@Component({
  components: {
    Button,
    VirtualCardCount
  }
})
export default class Dashboard extends Vue {
  @KeyCloakModule.Getter('isClient')
  public isClient!: any;
  @KeyCloakModule.Getter('isAdmin')
  public isAdmin!: any;

  @ProjectInfoModule.Getter('getProjectInfoList')
  public projectInfoList!: any;
  @ProjectInfoModule.Action('loadProjectInfo')
  public loadProjectInfo!: any;
  @ProjectInfoModule.Action('errorStatus')
  public errorStatus!: any;
  @SharedModule.Action('redirectFromSummaryPage')
  public redirectFromSummaryPage!: any;

  @SharedModule.Getter('isRedirectFromSummaryPage')
  public isRedirectFromSummaryPage!: boolean;

  private projectStatusList: any = projectStatus;
  private projectRolesList: any = projectRoles;

  private mounted() {
    this.loadProjectInfo();
  }

  private redirectToProject(project: any) {
    if (project.statusId === projectStatus.dev) {
      this.redirectFromSummaryPage(false);
    }
    this.$router.push(`/project-container/${project.id}`);
  }
  private getStatusClass(statusId: number) {
    let classToadd = ' bc-dev-project ';
    if (statusId > 2) {
      classToadd = ' bc-live-req-project ';
    } else if (statusId > 6) {
      classToadd = ' bc-live-project';
    }
    return classToadd;
  }
}
</script>

<style lang="scss" scoped>
@import './../../assets/styles/theme.scss';
.table-head {
  background-color: $BCgovBlue5 !important;
  color: $BCgovWhite !important;
  & tr {
    & th {
      color: $BCgovWhite !important;
      font-size: 14px;
    }
  }
}
</style>
