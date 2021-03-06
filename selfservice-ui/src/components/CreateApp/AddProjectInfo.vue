/** * Project information */
<template>
  <v-card class="mx-auto outer-card">
    <v-card class="mx-auto">
      <v-app-bar dark class="bc-subtitle">
        <v-btn icon @click="$router.push('/dashboard/')" aria-label="Back Button">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <h1 class="bc-h1-sub-ttile">
          {{
          $t('projectInfo.ProjectInfoTitle')
          }}
        </h1>
        <v-spacer></v-spacer>
      </v-app-bar>
      <v-form ref="form" v-model="form">
        <v-container>
          <v-row dense>
            <v-col cols="12" md="12">
              <v-card class="pa-8 pt-6 ma-3">
                <v-card-subtitle
                  class="text-left bc-padding-left-0 page-info"
                  v-html="$t('projectInfo.ProjectInfoTitleInfo')"
                ></v-card-subtitle>

                <Input
                  v-model="organizationName"
                  :label="$t('projectInfo.OrganizationName')"
                  type="text"
                  :rules="[
                    rules.required,
                    rules.length(2),
                    rules.maxLength(100),
                  ]"
                  :helpText="$t('projectInfo.OrganizationNameHint')"
                  data-test-id="input-org-name"
                  id="input-org-name"
                />

                <Input
                  v-model="projectName"
                  :label="$t('projectInfo.projectName')"
                  type="text"
                  :rules="[
                    rules.required,
                    rules.length(2),
                    rules.maxLength(100),
                  ]"
                  :helpText="$t('projectInfo.projectNameHint')"
                  data-test-id="input-project-name"
                  id="input-project-name"
                />

                <TextArea
                  v-model="description"
                  :label="$t('projectInfo.Description')"
                  type="text"
                  :rules="[rules.required, rules.maxLength(500)]"
                  outlined
                  :helpText="$t('projectInfo.DescriptionHint')"
                  data-test-id="text-project-description"
                  id="text-project-description"
                />
              </v-card>
            </v-col>

            <v-col cols="12">
              <v-card flat>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <Button
                    @click="$router.push(`/project-container/${id}`)"
                    @keyup.enter="$router.push(`/project-container/${id}`)"
                    aria-label="Back Button"
                    secondary
                    v-if="!showWizardExperience()"
                    data-test-id="btn-cancel-project-info"
                  >{{ $t('projectInfo.btnCancel') }}</Button>
                  <Button
                    :disabled="!form"
                    :loading="isLoading"
                    class="white--text submit-project"
                    depressed
                    @click="submitProjectInfo"
                    @keyup.enter="submitProjectInfo"
                    data-test-id="btn-submit-project-info"
                  >
                    {{
                    $t(
                    showWizardExperience()
                    ? 'projectInfo.btnNext'
                    : 'projectInfo.btnSaveChanges'
                    )
                    }}
                  </Button>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card>
  </v-card>
</template>
<script lang="ts">
import { Component, Vue, Watch, Prop } from 'vue-property-decorator';
import { Getter, namespace, Action } from 'vuex-class';
import { ProjectInfoModel } from '@/models/ProjectInfoModel';
import Input from '@/Atomic/Input/Input.vue';
import TextArea from '@/Atomic/TextArea/TextArea.vue';
import Button from '@/Atomic/Button/Button.vue';
import validationRules from '@/config/validationRules';

const ProjectInfoModule = namespace('ProjectInfoModule');
const SharedModule = namespace('SharedModule');

@Component({ components: { Input, TextArea, Button } })
export default class AddProjectInfo extends Vue {
  @Prop({ default: '' })
  public id!: string;
  @Prop({ default: '' })
  public action!: string;

  @ProjectInfoModule.Getter('successStatus') public successStatus!: boolean;
  @ProjectInfoModule.Getter('errorStatus') public errorStatus!: boolean;
  @ProjectInfoModule.Action('addProjectInfo') public addProjectInfoStore!: any;
  @ProjectInfoModule.Action('loadProjectInfo')
  public loadProjectInfo!: any;
  @ProjectInfoModule.Getter('getSingleProjectInfo')
  public getSingleProjectInfo!: any;
  @ProjectInfoModule.Action('updateProjectInfo')
  public updateProjectInfoStore!: any;
  @ProjectInfoModule.Action('loadSingleProjectInfo')
  public loadSingleProjectInfo!: any;

  @SharedModule.Getter('isRedirectFromSummaryPage')
  public isRedirectFromSummaryPage!: boolean;
  @SharedModule.Action('redirectFromSummaryPage')
  public redirectFromSummaryPage!: any;

  public form: boolean = false;
  private isLoading: boolean = false;
  private organizationName: string = '';
  private projectName: string = '';
  private description: string = '';
  private isEditMode: boolean = false;
  /* istanbul ignore next */
  private rules = validationRules;

  @Watch('getSingleProjectInfo')
  private ongetSingleProjectInfoChanged(val: any) {
    this.updteEdit(val);
  }

  private submitProjectInfo() {
    const data: ProjectInfoModel = {
      organizationName: this.organizationName,
      projectName: this.projectName,
      description: this.description
    };

    if (this.isEditMode) {
      data.id = this.id;
      this.updateProjectInfoStore(data);
      if (!this.showWizardExperience()) {
        this.redirectFromSummaryPage(true);
      }
    } else {
      this.addProjectInfoStore(data);
      this.redirectFromSummaryPage(false);
    }
  }

  private updteEdit(val: any) {
    this.organizationName = val.organizationName;
    this.projectName = val.projectName;
    this.description = val.description;
    this.isEditMode = true;
  }

  private mounted() {
    this.isEditMode = false;
    if (this.id !== '') {
      this.isEditMode = true;
      this.loadSingleProjectInfo(this.id);
    }
  }

  private showWizardExperience() {
    if (this.isEditMode && this.isRedirectFromSummaryPage) {
      return false;
    }
    return true;
  }
}
</script>

<style lang="scss" scoped>
.black-color {
  color: #000 !important;
}
.page-info {
  padding-bottom: 0 !important;
}
.org-title {
  padding-top: 0 !important;
}
</style>
