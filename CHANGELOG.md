# Changelog

## [0.4.0](https://github.com/gmc-norr/st2-analysis/compare/v0.3.2...v0.4.0) (2026-03-13)


### Features

* add `get plumber arguments` action ([#48](https://github.com/gmc-norr/st2-analysis/issues/48)) ([c484e8a](https://github.com/gmc-norr/st2-analysis/commit/c484e8ac6aa0e422cd96e2e888e5150b6d0bbf55))
* add `make case id` action ([#47](https://github.com/gmc-norr/st2-analysis/issues/47)) ([fe6758b](https://github.com/gmc-norr/st2-analysis/commit/fe6758b2e22842f5f2a8e4e1ca2d263e7b861728))
* add `make raredisease samplesheet` action ([#49](https://github.com/gmc-norr/st2-analysis/issues/49)) ([996ea12](https://github.com/gmc-norr/st2-analysis/commit/996ea12efca0226a85a2af72a5f78bdd4f7609fc))
* add `update complete plumber analysis` workflow and rule ([#46](https://github.com/gmc-norr/st2-analysis/issues/46)) ([b28293b](https://github.com/gmc-norr/st2-analysis/commit/b28293bfe2d94deb8214b5047a33a8a17cc679dd))
* add `update incomplete plumber analysis` rule ([#44](https://github.com/gmc-norr/st2-analysis/issues/44)) ([9753a4c](https://github.com/gmc-norr/st2-analysis/commit/9753a4c1e220fb6d3cb54e31e5f2b5104b9eaae1))
* add rule to send a notification email when a plumber run ends ([#42](https://github.com/gmc-norr/st2-analysis/issues/42)) ([3d9d5d2](https://github.com/gmc-norr/st2-analysis/commit/3d9d5d227f02533aae3cb686cea867c65249b614))


### Bug Fixes

* take notification email from datastore instead of config parameter ([#50](https://github.com/gmc-norr/st2-analysis/issues/50)) ([9609a54](https://github.com/gmc-norr/st2-analysis/commit/9609a54256d0e13c490e4616b5c3b814c568e292))

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
