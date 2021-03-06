/** * Add TechnicalReq */
<template>
  <v-card class="mx-auto outer-card">
    <v-card class="mx-auto">
      <v-app-bar dark class="bc-subtitle">
        <v-btn icon @click="goBack()" aria-label="Back Button">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <h1 class="bc-h1-sub-ttile">{{ $t('technicalRequirements.technicalTitle') }}</h1>
        <v-spacer></v-spacer>
      </v-app-bar>

      <v-form ref="form" v-model="form" class="pa-4 pt-6">
        <Loading v-if="isLoading" />
        <v-container v-else>
          <v-row dense>
            <v-col cols="12" md="12">
              <v-card class="pa-4 pt-6 mb-4">
                <v-card-title
                  class="headline bc-padding-left-0 text-capitalize"
                >{{ getSingleProjectInfo && getSingleProjectInfo.projectName }}</v-card-title>
                <v-card-subtitle
                  class="text-left bc-padding-left-0"
                  v-html="$t('technicalRequirements.technicalTitleInfo')"
                ></v-card-subtitle>
              </v-card>
              <v-card class="pa-4 pt-6">
                <Input
                  v-model="clientUri"
                  :label="$t('technicalRequirements.labelApplicationUrl')"
                  type="text"
                  :rules="[rules.required, rules.url, rules.maxLength(500)]"
                  :helpText="$t('technicalRequirements.inputAppText')"
                  data-test-id="input-app-url"
                  id="input-app-url"
                />

                <div
                  class="text-left my-1 bc-form-text"
                >{{ $t('technicalRequirements.labelRedirectUrl') }}</div>
                <div
                  v-for="(redirectUri, index) in redirectUris"
                  v-bind:key="index"
                  class="row v-form px-4 pr-lg-0"
                >
                  <div class="redirect-div">
                    <Input
                      v-model="redirectUris[index]"
                      type="text"
                      :rules="[rules.required, rules.urlLocalHost]"
                      class="addUri"
                      outlined
                      :data-test-id="`input-redirect-url${index}`"
                      :id="`input-redirect-url${index}`"
                    />
                  </div>
                  <div class="clear-icon">
                    <v-icon
                      class="ml-2"
                      large
                      @click="clearUri(index)"
                      @keyup.enter="clearUri(index)"
                      tabindex="0"
                      :aria-label="$t('technicalRequirements.ariaLabelRedirectUrlDelete')"
                    >mdi-close</v-icon>
                  </div>
                </div>

                <div
                  @click="addUri()"
                  @keyup.enter="addUri()"
                  class="add-url text-left"
                  tabindex="0"
                  role="button"
                >{{ $t('technicalRequirements.AddURI') }}</div>
                <v-card-title
                  class="text-left bc-padding-left-0"
                >{{ $t('technicalRequirements.labelTestMethod') }}</v-card-title>
                <v-card-subtitle
                  class="text-left bc-padding-left-0"
                >{{ $t('technicalRequirements.labelTestMethodHint') }}</v-card-subtitle>

                <v-card-subtitle class="text-left bc-padding-left-0">
                  <v-radio-group
                    v-model="signingEncryptionType"
                    :mandatory="false"
                    data-test-id="radio-algoritham-base"
                    role="radiogroup"
                    :aria-labelledby="$t('technicalRequirements.labelRadioGroup')"
                  >
                    <v-radio
                      :label="$t('technicalRequirements.labelSignedJWT')"
                      :value="algorithamBase.SignedJWT"
                      data-test-id="radio-algoritham-base-signed-jwt"
                      class="bc-form-radio"
                    ></v-radio>
                    <div
                      class="small-hint radio-help"
                    >{{ $t('technicalRequirements.SignedJWTHint') }}</div>
                    <div
                      class="row pad-radio"
                      v-if="signingEncryptionType === algorithamBase.SignedJWT"
                    >
                      <div class="col-12 col-md-5">
                        <Select
                          v-model="signedResponseAlg"
                          :label="
                            $t('technicalRequirements.labelSignedResponseAlg')
                          "
                          :items="signedAlg"
                          :rules="[rules.required]"
                          outlined
                          :helpText="
                            $t(
                              'technicalRequirements.labelSignedResponseAlgHint'
                            )
                          "
                          data-test-id="select-signed-response-alg"
                        />
                      </div>
                    </div>

                    <v-radio
                      :label="$t('technicalRequirements.labelSecureJWT')"
                      :value="algorithamBase.SecureJWT"
                      data-test-id="radio-algoritham-base-secure-jwt"
                      class="bc-form-radio"
                    ></v-radio>
                    <div
                      class="small-hint radio-help"
                    >{{ $t('technicalRequirements.SecureJWTHint') }}</div>
                  </v-radio-group>
                </v-card-subtitle>
                <div v-if="signingEncryptionType === algorithamBase.SecureJWT" class="pad-radio">
                  <Input
                    v-model="jwksUri"
                    :label="$t('technicalRequirements.labelJWKSUrl')"
                    type="text"
                    :rules="[rules.required, rules.url, rules.maxLength(500)]"
                    :helpText="$t('technicalRequirements.JWKSText')"
                    data-test-id="select-jwks-url"
                    id="select-jwks-url"
                  />
                  <div class="row">
                    <div class="col-12 col-md-4">
                      <Select
                        v-model="encryptedResponseEnc"
                        :label="
                          $t('technicalRequirements.labelEncryptedResponseEnc')
                        "
                        :items="encryptedEnc"
                        :rules="[rules.required]"
                        outlined
                        :helpText="
                          $t(
                            'technicalRequirements.labelEncryptedResponseEncHint'
                          )
                        "
                        helpClass="mb-9"
                        data-test-id="select-encrypted-response-enc"
                        id="select-encrypted-response-enc"
                      />
                    </div>
                    <div class="col-12 col-md-4">
                      <Select
                        v-model="encryptedResponseAlg"
                        :label="
                          $t('technicalRequirements.labelEncryptedResponseAlg')
                        "
                        :items="encryptedAlg"
                        :rules="[rules.required]"
                        outlined
                        :helpText="
                          $t(
                            'technicalRequirements.labelEncryptedResponseAlgHint'
                          )
                        "
                        helpClass="mb-9"
                        data-test-id="select-encrypted-response-alg"
                      />
                    </div>
                    <div class="col-12 col-md-4">
                      <Select
                        v-model="signedResponseAlg"
                        :label="
                          $t('technicalRequirements.labelSignedResponseAlg')
                        "
                        :items="signedAlg"
                        :rules="[rules.required]"
                        outlined
                        :helpText="
                          $t('technicalRequirements.labelSignedResponseAlgHint')
                        "
                        helpClass="mb-3"
                        data-test-id="select-signed-response-enc"
                      />
                    </div>
                  </div>
                </div>
                <!-- </v-form> -->
                <v-divider></v-divider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <Button
                    @click="goBack()"
                    @keyup.enter="goBack()"
                    aria-label="Back Button"
                    secondary
                    data-test-id="btn-cancel-technical-req"
                  >
                    {{
                    $t(
                    showWizardExperience()
                    ? 'technicalRequirements.btnBack'
                    : 'technicalRequirements.btnCancel'
                    )
                    }}
                  </Button>
                  <Button
                    :disabled="!form"
                    :loading="isLoading"
                    class="white--text submit-req ml-6"
                    depressed
                    @click="addTechnicalReq()"
                    @keyup.enter="addTechnicalReq()"
                    data-test-id="btn-submit-technical-req"
                  >
                    {{
                    $t(
                    showWizardExperience()
                    ? 'technicalRequirements.btnNext'
                    : 'technicalRequirements.btnSaveChanges'
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
import Input from '@/Atomic/Input/Input.vue';
import Button from '@/Atomic/Button/Button.vue';
import Select from '@/Atomic/Select/Select.vue';
import validationRules from '@/config/validationRules';
import Loading from '@/Atomic/Loading/Loading.vue';
import { algorithmBase } from '@/constants/enums';

import {
  signedAlgorithm,
  encryptedAlgorithm,
  encryptedEncoding
} from '@/constants/algorithm';
import { TechnicalReqModel } from '@/models/TechnicalReqModel';
const TechnicalReqModule = namespace('TechnicalReqModule');
const ProjectInfoModule = namespace('ProjectInfoModule');
const SharedModule = namespace('SharedModule');

@Component({
  components: { Input, Button, Select, Loading }
})
export default class AddTechnicalReq extends Vue {
  @Prop({ default: 0 })
  public id!: number;
  @Prop({ default: '' })
  public action!: string;

  @TechnicalReqModule.Getter('successStatus') public successStatus!: boolean;
  @TechnicalReqModule.Getter('errorStatus') public errorStatus!: boolean;
  @TechnicalReqModule.Action('addTechnicalReq')
  public addTechnicalReqStore!: any;
  @TechnicalReqModule.Getter('getTechnicalReq')
  public getTechnicalReq!: any;
  @TechnicalReqModule.Action('updateTechnicalReq')
  public updateTechnicalReqStore!: any;
  @TechnicalReqModule.Action('loadTechnicalReqDetails')
  public loadTechnicalReqDetails!: any;
  @TechnicalReqModule.Getter('isLoading') public isLoading!: boolean;

  @ProjectInfoModule.Getter('getSingleProjectInfo')
  public getSingleProjectInfo!: any;
  @ProjectInfoModule.Action('loadSingleProjectInfo')
  public loadSingleProjectInfo!: any;
  @SharedModule.Action('redirectFromSummaryPage')
  public redirectFromSummaryPage!: any;
  @SharedModule.Getter('isRedirectFromSummaryPage')
  public isRedirectFromSummaryPage!: boolean;

  public form: boolean = false;
  private projectId: number = this.id || 0;
  private TechnicalReqId: number = 0;
  private clientUri: string = '';
  private redirectUris: any = [''];
  private jwksUri: string = '';
  private encryptedResponseEnc: string = 'A256GCM';
  private encryptedResponseAlg: string = 'RSA-OAEP';
  private signedResponseAlg: string = 'RS256';
  private signedAlg: any = signedAlgorithm;
  private encryptedAlg: any = encryptedAlgorithm;
  private encryptedEnc: any = encryptedEncoding;
  private blockRemoval = true;
  private signingEncryptionType: number = algorithmBase.SignedJWT;
  private algorithamBase: any = algorithmBase;

  // private id: string = '';
  private isEditMode: boolean = false;
  /* istanbul ignore next */
  private rules = validationRules;

  @Watch('getTechnicalReq')
  private ongetTechnicalReqChanged(val: any) {
    this.updteEdit(val);
  }

  @Watch('getSingleProjectInfo')
  private ongetSingleProjectInfoChanged(val: any) {
    this.projectId = this.getSingleProjectInfo.id;
  }

  private addTechnicalReq() {
    const data: TechnicalReqModel = {
      projectId: this.projectId,
      clientUri: this.clientUri,
      redirectUris: this.redirectUris,
      signingEncryptionType: this.signingEncryptionType,
      jwksUri:
        this.signingEncryptionType === algorithmBase.SecureJWT
          ? this.jwksUri
          : '',
      encryptedResponseAlg:
        this.signingEncryptionType === algorithmBase.SecureJWT
          ? this.encryptedResponseAlg
          : null,
      encryptedResponseEnc:
        this.signingEncryptionType === algorithmBase.SecureJWT
          ? this.encryptedResponseEnc
          : null,
      signedResponseAlg: this.signedResponseAlg
    };

    if (this.isEditMode && this.TechnicalReqId !== 0) {
      data.id = this.TechnicalReqId;
      this.updateTechnicalReqStore(data);
    } else {
      this.addTechnicalReqStore(data);
    }
  }

  private updteEdit(val: any) {
    this.projectId = val.projectId || this.projectId;
    this.clientUri = val.clientUri;
    this.redirectUris = val.redirectUris || this.redirectUris;
    this.jwksUri = val.jwksUri;
    this.encryptedResponseEnc =
      val.encryptedResponseEnc || this.encryptedResponseEnc;
    this.encryptedResponseAlg =
      val.encryptedResponseAlg || this.encryptedResponseAlg;
    this.signedResponseAlg = val.signedResponseAlg || this.signedResponseAlg;
    this.TechnicalReqId = val.id || 0;
    this.isEditMode = true;
    this.signingEncryptionType =
      val.signingEncryptionType || this.signingEncryptionType;
  }

  private mounted() {
    this.isEditMode = false;

    if (this.id !== 0) {
      this.isEditMode = true;
      this.loadTechnicalReqDetails(this.id);
    }
    if (this.getSingleProjectInfo && this.getSingleProjectInfo.id) {
      this.projectId = this.getSingleProjectInfo.id;
    } else {
      this.loadSingleProjectInfo(this.id);
    }
  }
  private goBack() {
    const redirectPage = this.showWizardExperience()
      ? `/project/${this.projectId}/team/`
      : `/project-container/${this.projectId}/`;
    this.redirectFromSummaryPage(false);
    this.$router.push(redirectPage);
  }
  private showWizardExperience() {
    if (this.isEditMode && this.isRedirectFromSummaryPage) {
      return false;
    }
    return true;
  }

  private addUri() {
    const checkEmptyLines = this.redirectUris.filter((uri: any) => uri === '');

    if (checkEmptyLines.length >= 1 || this.redirectUris.length >= 10) {
      return;
    }

    this.redirectUris.push('');
  }
  private clearUri(uriId: number) {
    this.blockRemoval = this.redirectUris.length <= 1;
    if (!this.blockRemoval) {
      this.redirectUris.splice(uriId, 1);
    }
  }
}
</script>
<style lang="scss" scoped>
@import './../../assets/styles/theme.scss';
.pad-radio {
  padding-left: 33px;
}
.pad-0 {
  padding: 0;
}
.radio-help {
  margin-top: -11px;
  margin-left: 30px;
  margin-bottom: 10px;
}
.add-url {
  margin-left: 7px;
  color: $BCgovBlue10;
  cursor: pointer;
}
.redirect-div {
  width: 90%;
  @include sm {
    width: 94%;
  }
  @include md {
    width: 95%;
  }
}
.clear-icon {
  position: absolute;
  margin-top: 10px;
  right: 15px;
}
</style>
