/** * TextArea atomic component * TextArea allow users to carry out an important
action on your service, such as Download or Submit. */

<template>
  <div class="bc-form-text">
    <label class="text-left my-1" :for="id">{{label}}</label>
    <div class="text-left mb-1 subtitle-2 bc-help-text" v-if="helpText !==''">{{helpText}}</div>
    <v-textarea :value="value" @input="input" v-bind="$attrs" solo :id="id"></v-textarea>
  </div>
  <!-- outlined -->
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

/**
 *
 * @displayName  Input
 */

@Component
export default class TextArea extends Vue {
  /**
   * The counter for the input.
   *
   */
  @Prop({
    default: ''
  })
  private counter!: string | number;

  /**
   * The type for the input.
   * @values input, password
   */
  @Prop({
    default: 'text'
  })
  private type!: string;

  /**
   *  value for input
   */
  @Prop({
    default: ''
  })
  private value!: string;

  /**
   *  label text
   */
  @Prop({
    default: ''
  })
  private label!: string;

  /**
   *  required
   */
  @Prop({
    default: false
  })
  private required!: boolean;
  /**
   *  helpText text
   */
  @Prop({
    default: ''
  })
  private helpText!: string;
  /**
   *  id
   */
  @Prop({
    default: ''
  })
  private id!: string;
  /**
   * input
   * @description update value on key up or blur
   * @param {string} inputval
   */
  private input(inputval: string) {
    this.$emit('input', inputval);
  }
}
</script>

<style lang="scss" scoped>
// @import './../../assets/styles/theme.scss';
.bc-form-text {
  text-align: left;
}
</style>
