import React from "react";
import {
  NesicaMaintenancePopup,
  EamuseMaintenancePopup,
  AimeIntlMaintenanceInfo,
  AllnetPrivateServerWarning,
} from "./NoteModals";
import i18next from 'i18next';

export const GameNotes = (isMoe: boolean): Record<string, React.ReactNode> => ({
  sdvx: (
    <>
      <ul className={`mt-2 ${isMoe ? "text-pink-900" : "text-white"}`}>
        <li>{i18next.t('gamenotes.sdvx.premium_generator')}</li>
        <li>{i18next.t('gamenotes.sdvx.voltefactory')}</li>
        <li>{i18next.t('gamenotes.sdvx.cover_art')}</li>
        <li>{i18next.t('gamenotes.sdvx.crossregion')}</li>
      </ul>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.common.na_service_note')}
        <br />
        {i18next.t('gamenotes.common.private_network_note')}
      </p>
    </>
  ),
  iidx: (
    <>
      <ul className={`mt-2 ${isMoe ? "text-pink-900" : "text-white"}`}>
        <li>{i18next.t('gamenotes.iidx.features')}</li>
      </ul>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.common.na_service_note')}
        <br />
        {i18next.t('gamenotes.common.private_network_note')}
      </p>
    </>
  ),
  gitadora: (
    <>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.common.na_service_note')}
        <br />
        {i18next.t('gamenotes.common.private_network_note')}
      </p>
    </>
  ),
  dance_rush: (
    <>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.common.na_service_note')}
        <br />
        {i18next.t('gamenotes.common.private_network_note')}
      </p>
    </>
  ),
  dance_around: (
    <>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.common.na_service_note')}
        <br />
        {i18next.t('gamenotes.common.private_network_note')}
      </p>
    </>
  ),
  polaris_chord: (
    <>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.polaris_chord.online_note')}
      </p>
    </>
  ),
  ddr: (
    <>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.common.na_service_note')}
        <br />
        {i18next.t('gamenotes.common.private_network_note')}
        <br />
        {i18next.t('gamenotes.ddr.maintenance_note')}
      </p>
    </>
  ),
  jubeat: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.jubeat.online_note')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.common.private_network_note')}
      </p>
    </>
  ),
  popn_music: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.popn_music.online_note')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.common.private_network_note')}
      </p>
    </>
  ),
  nostalgia: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.nostalgia.online_note')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.common.private_network_note')}
      </p>
    </>
  ),
  chunithm_jp: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.common.japan_only_note')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.common.international_note')}
      </p>
    </>
  ),
  maimaidx_jp: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.common.japan_only_note')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.common.international_note')}
      </p>
    </>
  ),
  ongeki_jp: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.ongeki_jp.japan_only')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.ongeki_jp.private_network')}
      </p>
      <div className="flex justify-center">
        <AllnetPrivateServerWarning isMoe={isMoe} />
      </div>
    </>
  ),
  idac: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.idac.japan_only')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.idac.private_network')}
      </p>
    </>
  ),
  chunithm_intl: (
    <>
      <ul className={`mt-2 ${isMoe ? "text-pink-900" : "text-white"}`}>
        <li>{i18next.t('gamenotes.chunithm_intl.updates')}</li>
      </ul>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.chunithm_intl.no_service')}{" "}
        <a
          className="underline"
          href="https://location.am-all.net/alm/location?gm=104&lang=en"
        >
          {i18next.t('gamenotes.chunithm_intl.regions_link')}
        </a>
      </p>
      <div className="flex justify-center">
        <AllnetPrivateServerWarning isMoe={isMoe} />
      </div>
    </>
  ),
  maimaidx_intl: (
    <>
      <div className="flex justify-center">
        <AimeIntlMaintenanceInfo isMoe={isMoe} />
      </div>
      <ul className={`mt-2 ${isMoe ? "text-pink-900" : "text-white"}`}>
        <li>{i18next.t('gamenotes.maimaidx_intl.updates')}</li>
        <li>{i18next.t('gamenotes.maimaidx_intl.charts')}</li>
      </ul>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.maimaidx_intl.service')}{" "}
        <a
          className="underline"
          href="https://location.am-all.net/alm/location?gm=98"
        >
          {i18next.t('gamenotes.maimaidx_intl.regions_link')}
        </a>
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.maimaidx_intl.no_eu')}
      </p>
      <div className="flex justify-center">
        <AllnetPrivateServerWarning isMoe={isMoe} />
      </div>
    </>
  ),
  music_diver: (
    <>
      <div className="flex justify-center">
        <NesicaMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.music_diver.online_service')}
      </p>
    </>
  ),
  street_fighter: (
    <>
      <div className="flex justify-center">
        <NesicaMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        {i18next.t('gamenotes.street_fighter.online_service')}
      </p>
    </>
  ),
  wacca_plus: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-white"} text-center`}
      >
        {i18next.t('gamenotes.wacca_plus.community')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.wacca_plus.note')}
      </p>
    </>
  ),
  museca_plus: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-white"} text-center`}
      >
        {i18next.t('gamenotes.museca_plus.community')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.museca_plus.note')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        <a className="underline" href="https://museca.plus/downloads">
          {i18next.t('gamenotes.museca_plus.download')}
        </a>
      </p>
    </>
  ),
  rb_deluxe_plus: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-white"} text-center`}
      >
        {i18next.t('gamenotes.rb_deluxe_plus.community')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.rb_deluxe_plus.note')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.rb_deluxe_plus.feed_note')}
      </p>
    </>
  ),
  taiko: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-white"} text-center`}
      >
        {i18next.t('gamenotes.taiko.version_note')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.taiko.maintenance')}<br/>
        {i18next.t('gamenotes.taiko.usa_note')}
      </p>
    </>
  ),
  wmmt: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-white"} text-center`}
      >
        {i18next.t('gamenotes.wmmt.feed')}
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        {i18next.t('gamenotes.wmmt.version')}
      </p>
    </>
  ),
});
