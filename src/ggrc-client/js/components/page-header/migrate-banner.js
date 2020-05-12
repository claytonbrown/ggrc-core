/*
 Copyright (C) 2020 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import canStache from 'can-stache';
import canComponent from 'can-component';

const DEFAULT_BANNER = {
  font_color: 'ffffff',
  bg_color: '31d018',
  message: 'This is default banner\'s notice',
};
const MIGRATE_BANNER = GGRC.alert_banner ? GGRC.alert_banner : DEFAULT_BANNER;

export default canComponent.extend({
  tag: 'migrate-banner',
  view: canStache(
    `<div style="
      color: #${MIGRATE_BANNER.font_color};
      background-color: #${MIGRATE_BANNER.bg_color};
      width: 100%;
      height: 47px;
      text-align: center">
      ${MIGRATE_BANNER.message}
    </div>`
  ),
});
