/** * ListPackage component */

<template>
  <v-card class="mx-auto outer-card">
    <v-toolbar flat class="bc-subtitle" dark>
      <v-btn icon @click="goBack()" :aria-label="$t('selectPackage.btnBack')">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <h1 class="bc-h1-sub-ttile">{{ $t('selectPackage.pagetitle') }}</h1>
      <div class="flex-grow-1"></div>

      <div class="flex-grow-1"></div>
    </v-toolbar>
    <v-divider></v-divider>

    <v-item-group mandatory :value="slectedPackage">
      <v-container>
        <v-row class="ma-5">
          <v-col cols="12" flat>
            <Alert type="error" v-if="errorStatus" class="alert-top">Something went wrong...</Alert>
            <v-card flat>
              <v-list-item-content v-html="$t('selectPackage.pagetitleInfo')"></v-list-item-content>
              <!-- <v-list-item-content>{{
                $t('selectPackage.package2')
              }}</v-list-item-content>
              <v-list-item-content>{{
                $t('selectPackage.package3')
              }}</v-list-item-content>-->
            </v-card>
          </v-col>

          <v-col v-for="(packageData, idx) in getPackageList" :key="idx" cols="12" md="12">
            <v-item v-slot:default="{ active }" :value="packageData.id" class="select-package">
              <v-card
                class="d-flex align-center pa-4 select-package"
                :class="active ? 'active-bg' : ''"
                @click="selectedPackage(packageData.id)"
                @keyup.enter="selectedPackage(packageData.id)"
                :data-test-id="`select-package-${packageData.id}`"
              >
                <v-list-item three-line>
                  <v-list-item-content>
                    <v-list-item-title class="headline mb-1">
                      {{
                      packageData.packageName
                      }}
                    </v-list-item-title>
                    <v-list-item-subtitle class="mb-2">
                      {{
                      $t('selectPackage.description')
                      }}
                    </v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-for="claimName in packageData.claimNames"
                      :key="claimName"
                      class="ml-3"
                    >
                      <v-icon color="#969798" x-small>mdi-check-circle</v-icon>
                      {{ claimName }}
                    </v-list-item-subtitle>
                    <v-list-item-subtitle class="mt-3">
                      {{
                      packageData.description
                      }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-spacer></v-spacer>
                <div v-if="!active" class="text-center mr-5">
                  <v-icon color="#eae9e9" x-large>mdi-check-circle-outline</v-icon>
                  <!-- Select this package -->
                </div>
                <div v-if="active" class="display-3 flex-grow-1 text-center mr-5">
                  <v-icon color="green" x-large>mdi-check-circle</v-icon>
                </div>
                <!-- </v-scroll-y-transition> -->
              </v-card>
            </v-item>
          </v-col>
        </v-row>
      </v-container>
    </v-item-group>
    <v-col cols="12">
      <v-card flat class="ma-5">
        <v-divider></v-divider>
        <v-card-actions>
          <!-- <v-btn text @click="$refs.form.reset()">Clear</v-btn> -->
          <v-spacer></v-spacer>
          <Button
            @click="goBack"
            @keyup.enter="goBack"
            :aria-label="$t('selectPackage.btnBack')"
            secondary
            class="back-btn"
            data-test-id="btn-cancel-package-select"
          >
            {{
            $t(
            showWizardExperience()
            ? 'selectPackage.btnBack'
            : 'selectPackage.btnCancel'
            )
            }}
          </Button>
          <Button
            :disabled="!slectedPackage"
            :loading="isLoading"
            class="white--text submit-package ml-6"
            depressed
            @click="submitPackage"
            @keyup.enter="submitPackage"
            data-test-id="btn-submit-package-select"
          >
            {{
            $t(
            showWizardExperience()
            ? 'selectPackage.btnNext'
            : 'selectPackage.btnSaveChanges'
            )
            }}
          </Button>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-card>
</template>
<script lang="ts">
import { Component, Vue, Watch, Prop } from 'vue-property-decorator';
import { Getter, namespace, Action } from 'vuex-class';
import Button from '@/Atomic/Button/Button.vue';
import Alert from '@/Atomic/Alert/Alert.vue';

const PackageAndTestModule = namespace('PackageAndTestModule');
const SharedModule = namespace('SharedModule');
const TechnicalReqModule = namespace('TechnicalReqModule');

@Component({
  components: {
    Button,
    Alert
  }
})
export default class ListPackage extends Vue {
  @Prop({ default: 0 })
  public id!: number;
  @PackageAndTestModule.Getter('successStatus') public successStatus!: boolean;
  @PackageAndTestModule.Getter('errorStatus') public errorStatus!: boolean;
  @PackageAndTestModule.Action('loadPackage') public loadPackage!: any;
  @PackageAndTestModule.Getter('getPackageList') public getPackageList!: [];
  @PackageAndTestModule.Action('clearStatus') public clearStatus!: any;
  @PackageAndTestModule.Action('addPackagetoProject')
  public addPackagetoProject!: any;
  @SharedModule.Action('redirectFromSummaryPage')
  public redirectFromSummaryPage!: any;
  @SharedModule.Getter('isRedirectFromSummaryPage')
  public isRedirectFromSummaryPage!: boolean;

  @TechnicalReqModule.Action('loadTechnicalReqDetails')
  public loadTechnicalReqDetails!: any;
  @TechnicalReqModule.Getter('getTechnicalReq')
  public getTechnicalReq!: any;
  @TechnicalReqModule.Getter('isLoading') public isLoading!: boolean;

  private slectedPackage: number = 1;
  // private isLoading: boolean = false;
  private projectId: number = this.id || 0;

  @Watch('successStatus')
  private onStatusChanged(val: any, oldVal: any) {
    setTimeout(this.clearStatus, 3000);
  }
  @Watch('getTechnicalReq')
  private ongetTechnicalReqChanged(val: any) {
    this.slectedPackage = val.scopePackageId || this.slectedPackage;
  }

  private mounted() {
    this.loadPackage();
    if (this.id !== 0) {
      // this.isEditMode = true;
      this.loadTechnicalReqDetails(this.id);
    }
  }
  private selectedPackage(packageVal: number) {
    this.slectedPackage = packageVal;
  }
  private submitPackage() {
    // add package to project com ehere
    this.addPackagetoProject({
      slectedPackage: this.slectedPackage,
      projectId: this.projectId
    });
  }

  private goBack() {
    const redirectPage = this.showWizardExperience()
      ? `/project/${this.projectId}/technical/`
      : `/project-container/${this.projectId}/`;

    this.redirectFromSummaryPage(false);
    this.$router.push(redirectPage);
  }
  private showWizardExperience() {
    if (this.isRedirectFromSummaryPage) {
      return false;
    }
    return true;
  }
}
</script>

<style lang="scss" scoped>
@import './../../assets/styles/theme.scss';
.active-bg {
  background-color: $BCgovActiveBg;
}
</style>
