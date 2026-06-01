# Changelog

## [0.4.2](https://github.com/gmc-norr/st2-analysis/compare/v0.4.1...v0.4.2) (2026-06-01)


### Bug Fixes

* **update_complete_plumber_analysis:** update path to analysis in a seperate step from adding the output files ([#82](https://github.com/gmc-norr/st2-analysis/issues/82)) ([9c917fd](https://github.com/gmc-norr/st2-analysis/commit/9c917fd1ef06cc8163784129db84ee6d9654e6dc))

## [0.4.1](https://github.com/gmc-norr/st2-analysis/compare/v0.4.0...v0.4.1) (2026-05-29)


### Bug Fixes

* **get_plumber_arguments:** only compare major version of application profiles ([#78](https://github.com/gmc-norr/st2-analysis/issues/78)) ([0121c71](https://github.com/gmc-norr/st2-analysis/commit/0121c7181abbb9157f11c7060001aa326de62887))
* **plumber_analysis:** limit concurrency to 1 and increase pause to 30s ([#77](https://github.com/gmc-norr/st2-analysis/issues/77)) ([e280318](https://github.com/gmc-norr/st2-analysis/commit/e2803183805316dbe44adaa59fca8aa91e275cec))
* **plumber_analysis:** only email about failing to get sample info from iGene if the sample id starts with "Seq" ([#75](https://github.com/gmc-norr/st2-analysis/issues/75)) ([b732908](https://github.com/gmc-norr/st2-analysis/commit/b7329086f51a37f9f126d22ca8e69d3640db7d9c))
* **plumber_analysis:** redirect plumber's stderr  ([#76](https://github.com/gmc-norr/st2-analysis/issues/76)) ([471896c](https://github.com/gmc-norr/st2-analysis/commit/471896c9dc654b834eed82c439141f3009a7dd5d))
* rd workflow checks flowcell instead of number of reads per sample ([#73](https://github.com/gmc-norr/st2-analysis/issues/73)) ([cd02a7d](https://github.com/gmc-norr/st2-analysis/commit/cd02a7d8f09ae705d81b047a0217f5e2f7ff0b4c))
* **update_complete_plumber_analysis:** increase rsync timeout and change flags to `-a --remove-source-files` ([#79](https://github.com/gmc-norr/st2-analysis/issues/79)) ([cb30a76](https://github.com/gmc-norr/st2-analysis/commit/cb30a7654831b346a054bd3007947e0cdc3d986f))

## [0.4.0](https://github.com/gmc-norr/st2-analysis/compare/v0.3.2...v0.4.0) (2026-05-20)


### Features

* add `get pipeline input files` (for Cleve) action ([#51](https://github.com/gmc-norr/st2-analysis/issues/51)) ([ac5247c](https://github.com/gmc-norr/st2-analysis/commit/ac5247ce40c77280622f66fc39247b40a53a2328))
* add `get plumber arguments` action ([#48](https://github.com/gmc-norr/st2-analysis/issues/48)) ([c484e8a](https://github.com/gmc-norr/st2-analysis/commit/c484e8ac6aa0e422cd96e2e888e5150b6d0bbf55))
* add `make case id` action ([#47](https://github.com/gmc-norr/st2-analysis/issues/47)) ([fe6758b](https://github.com/gmc-norr/st2-analysis/commit/fe6758b2e22842f5f2a8e4e1ca2d263e7b861728))
* add `make raredisease samplesheet` action ([#49](https://github.com/gmc-norr/st2-analysis/issues/49)) ([996ea12](https://github.com/gmc-norr/st2-analysis/commit/996ea12efca0226a85a2af72a5f78bdd4f7609fc))
* add `update complete plumber analysis` workflow and rule ([#46](https://github.com/gmc-norr/st2-analysis/issues/46)) ([b28293b](https://github.com/gmc-norr/st2-analysis/commit/b28293bfe2d94deb8214b5047a33a8a17cc679dd))
* add `update incomplete plumber analysis` rule ([#44](https://github.com/gmc-norr/st2-analysis/issues/44)) ([9753a4c](https://github.com/gmc-norr/st2-analysis/commit/9753a4c1e220fb6d3cb54e31e5f2b5104b9eaae1))
* add rule to send a notification email when a plumber run ends ([#42](https://github.com/gmc-norr/st2-analysis/issues/42)) ([3d9d5d2](https://github.com/gmc-norr/st2-analysis/commit/3d9d5d227f02533aae3cb686cea867c65249b614))
* add start plumber workflows ([#39](https://github.com/gmc-norr/st2-analysis/issues/39)) ([6d488ed](https://github.com/gmc-norr/st2-analysis/commit/6d488ed1de34e4e0412631a735303e73ee5fc011))
* start scout workflow at the end of `update finished plumber analysis` workflow ([#57](https://github.com/gmc-norr/st2-analysis/issues/57)) ([9e0b856](https://github.com/gmc-norr/st2-analysis/commit/9e0b8567f459d4a19c3aba1a722d8ff875acc1a3))


### Bug Fixes

* `get plumber arguments` no longer checks if application is supported ([#72](https://github.com/gmc-norr/st2-analysis/issues/72)) ([a2b1630](https://github.com/gmc-norr/st2-analysis/commit/a2b1630dc89fcfdbb5dfb43c6d57c37f3ae185ea))
* change `make rd samplesheet` checks ([#59](https://github.com/gmc-norr/st2-analysis/issues/59)) ([9261da4](https://github.com/gmc-norr/st2-analysis/commit/9261da44c445725a811bbbfebff35a542ea25739))
* escape error message on plumber email rule ([#56](https://github.com/gmc-norr/st2-analysis/issues/56)) ([73132d2](https://github.com/gmc-norr/st2-analysis/commit/73132d2d3cdfa38946a52af2bb0bb207239361de))
* escape the message from plumber ([#53](https://github.com/gmc-norr/st2-analysis/issues/53)) ([33ec788](https://github.com/gmc-norr/st2-analysis/commit/33ec788d8a7c84fb92e61b7251f3e88c06a33e53))
* Formating of pipeline output files, with correct level ([#54](https://github.com/gmc-norr/st2-analysis/issues/54)) ([60d8da1](https://github.com/gmc-norr/st2-analysis/commit/60d8da1ae7f78bee3d266d6d801efbacab92d45f))
* match original pipeline names ([#55](https://github.com/gmc-norr/st2-analysis/issues/55)) ([56318ba](https://github.com/gmc-norr/st2-analysis/commit/56318baf8b837a0058dabef7fc78053c1aa28bae))
* rsync removes source files in the `update complete plumber analysis` workflow ([#70](https://github.com/gmc-norr/st2-analysis/issues/70)) ([04856e7](https://github.com/gmc-norr/st2-analysis/commit/04856e7ea7813a52356deb2c0ed2f360b551bfd5))
* scout output_path parameter uses variable ([#71](https://github.com/gmc-norr/st2-analysis/issues/71)) ([51567df](https://github.com/gmc-norr/st2-analysis/commit/51567df8006ed1328000fed6eb1224fba46b608b))
* take notification email from datastore instead of config parameter ([#50](https://github.com/gmc-norr/st2-analysis/issues/50)) ([9609a54](https://github.com/gmc-norr/st2-analysis/commit/9609a54256d0e13c490e4616b5c3b814c568e292))
* tumor evolution tests use correct email setup ([#58](https://github.com/gmc-norr/st2-analysis/issues/58)) ([8425dc0](https://github.com/gmc-norr/st2-analysis/commit/8425dc0a779b0004001ba12d8c8929dc2463e75a))

## [0.3.2](https://github.com/gmc-norr/st2-analysis/compare/v0.3.1...v0.3.2) (2025-03-14)


### Bug Fixes

* properly reset polling intervall on error recovery ([#32](https://github.com/gmc-norr/st2-analysis/issues/32)) ([8552132](https://github.com/gmc-norr/st2-analysis/commit/8552132899e31fd00fe39c0a59b58be18116f610))

## [0.3.1](https://github.com/gmc-norr/st2-analysis/compare/v0.3.0...v0.3.1) (2024-11-11)


### Bug Fixes

* catch encoding errors when reading watch file ([#27](https://github.com/gmc-norr/st2-analysis/issues/27)) ([24c03a4](https://github.com/gmc-norr/st2-analysis/commit/24c03a4d16aae541534edac05bc828296985d80b))
* correct trigger name for notification emails ([#30](https://github.com/gmc-norr/st2-analysis/issues/30)) ([ac916c2](https://github.com/gmc-norr/st2-analysis/commit/ac916c2fd0fbbdc3c9cd16088b173fffdf4a1a19))

## [0.3.0](https://github.com/gmc-norr/st2-analysis/compare/v0.2.4...v0.3.0) (2024-10-30)


### Features

* more general handling of windows mounts ([#24](https://github.com/gmc-norr/st2-analysis/issues/24)) ([5c8f284](https://github.com/gmc-norr/st2-analysis/commit/5c8f28454582d62a3e5ca0c7792fc2aea6183830))

## [0.2.4](https://github.com/gmc-norr/st2-analysis/compare/v0.2.3...v0.2.4) (2024-10-23)


### Bug Fixes

* add support for quoted paths ([0b9a978](https://github.com/gmc-norr/st2-analysis/commit/0b9a9782025e0b11f828fc95a01c8198848e1077))
* bug in excel file paths ([0690231](https://github.com/gmc-norr/st2-analysis/commit/06902316f34503d664f14a6d7886fc529bbb0b4b))

## [0.2.3](https://github.com/gmc-norr/st2-analysis/compare/v0.2.2...v0.2.3) (2024-10-21)


### Bug Fixes

* more general support for windows paths ([#19](https://github.com/gmc-norr/st2-analysis/issues/19)) ([413eefb](https://github.com/gmc-norr/st2-analysis/commit/413eefb97babd68fcce9b2f4292eb14686ad151b))

## [0.2.2](https://github.com/gmc-norr/st2-analysis/compare/v0.2.1...v0.2.2) (2024-04-15)


### Bug Fixes

* sensor crash when mount is missing ([#15](https://github.com/gmc-norr/st2-analysis/issues/15)) ([671c344](https://github.com/gmc-norr/st2-analysis/commit/671c344ad7d955e2dcd404ffa06f127ebfd1f0fa))

## [0.2.1](https://github.com/gmc-norr/st2-gmc-norr/compare/v0.2.0...v0.2.1) (2024-01-08)


### Bug Fixes

* fail if the report cannot be generated ([#7](https://github.com/gmc-norr/st2-gmc-norr/issues/7)) ([b2146aa](https://github.com/gmc-norr/st2-gmc-norr/commit/b2146aae65dac49f4e78039b02ce34d425540976))

## [0.2.0](https://github.com/gmc-norr/st2-gmc-norr/compare/v0.1.2...v0.2.0) (2024-01-05)


### Features

* ability to submit more than one report request at a time ([72a91d8](https://github.com/gmc-norr/st2-gmc-norr/commit/72a91d81c3e34faa98d89158edaceb561ca27970))
* add tumor evolution sensor ([#5](https://github.com/gmc-norr/st2-gmc-norr/issues/5)) ([72a91d8](https://github.com/gmc-norr/st2-gmc-norr/commit/72a91d81c3e34faa98d89158edaceb561ca27970))

## [0.1.2](https://github.com/gmc-norr/st2-gmc-norr/compare/v0.1.1...v0.1.2) (2023-09-19)


### Bug Fixes

* add tumor-evolution version to config schema ([efde1c9](https://github.com/gmc-norr/st2-gmc-norr/commit/efde1c962524508109dd6e0576f385384784aad7))

## [0.1.1](https://github.com/gmc-norr/st2-gmc-norr/compare/v0.1.0...v0.1.1) (2023-07-18)


### Bug Fixes

* pull tags when updating tumor-evolution repo ([d80c2e2](https://github.com/gmc-norr/st2-gmc-norr/commit/d80c2e20f52d92200ca7e57ea9ce6cffa6fc9cb6))

## 0.1.0 (2023-07-18)


### Bug Fixes

* get tumor evolution version from config ([39a339d](https://github.com/gmc-norr/st2-gmc-norr/commit/39a339dc197cf439613c04ff6beff62c40e838ab))


### Continuous Integration

* fix release-please action ([de1be40](https://github.com/gmc-norr/st2-gmc-norr/commit/de1be40cf3fdc04c7e0dc3d44af1358589953884))
