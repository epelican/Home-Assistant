import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import spi
from esphome.components import remote_transmitter
from esphome.const import CONF_ID

CODEOWNERS = ["@swoboda1337"]

DEPENDENCIES = ["spi"]

CONF_PA_POWER = 'pa_power'
CONF_PA_PIN = 'pa_pin'
CONF_NSS_PIN = 'nss_pin'
CONF_RST_PIN = 'rst_pin'
CONF_FREQUENCY = "frequency"
CONF_MODULATION = "modulation"
CONF_RX_FLOOR = "rx_floor"
CONF_RX_START = "rx_start"
CONF_RX_BANDWIDTH = "rx_bandwidth"
CONF_TRANSMITTER_ID = 'transmitter_id'

sx127x_ns = cg.esphome_ns.namespace("sx127x")
SX127x = sx127x_ns.class_("SX127x", cg.Component, spi.SPIDevice)
SX127xMod = sx127x_ns.enum("SX127xMod")
SX127xRxBw = sx127x_ns.enum("SX127xRxBw")
SX127xPaPin = sx127x_ns.enum("SX127xPaPin")

PA_PIN = {
    "RFO": SX127xPaPin.RFO,
    "PA_BOOST": SX127xPaPin.PA_BOOST,
}

MOD = {
    "FSK": SX127xMod.MODULATION_FSK,
    "OOK": SX127xMod.MODULATION_OOK,
}

RX_BW = {
    "2_6kHz": SX127xRxBw.RX_BANDWIDTH_2_6,
    "3_1kHz": SX127xRxBw.RX_BANDWIDTH_3_1,
    "3_9kHz": SX127xRxBw.RX_BANDWIDTH_3_9,
    "5_2kHz": SX127xRxBw.RX_BANDWIDTH_5_2,
    "6_3kHz": SX127xRxBw.RX_BANDWIDTH_6_3,
    "7_8kHz": SX127xRxBw.RX_BANDWIDTH_7_8,
    "10_4kHz": SX127xRxBw.RX_BANDWIDTH_10_4,
    "12_5kHz": SX127xRxBw.RX_BANDWIDTH_12_5,
    "15_6kHz": SX127xRxBw.RX_BANDWIDTH_15_6,
    "20_8kHz": SX127xRxBw.RX_BANDWIDTH_20_8,
    "25_0kHz": SX127xRxBw.RX_BANDWIDTH_25_0,
    "31_3kHz": SX127xRxBw.RX_BANDWIDTH_31_3,
    "41_7kHz": SX127xRxBw.RX_BANDWIDTH_41_7,
    "50_0kHz": SX127xRxBw.RX_BANDWIDTH_50_0,
    "62_5kHz": SX127xRxBw.RX_BANDWIDTH_62_5,
    "83_3kHz": SX127xRxBw.RX_BANDWIDTH_83_3,
    "100_0kHz": SX127xRxBw.RX_BANDWIDTH_100_0,
    "125_0kHz": SX127xRxBw.RX_BANDWIDTH_125_0,
    "166_7kHz": SX127xRxBw.RX_BANDWIDTH_166_7,
    "200_0kHz": SX127xRxBw.RX_BANDWIDTH_200_0,
    "250_0kHz": SX127xRxBw.RX_BANDWIDTH_250_0
}

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(SX127x),
            cv.Required(CONF_RST_PIN): pins.internal_gpio_output_pin_schema,
            cv.Required(CONF_NSS_PIN): pins.internal_gpio_output_pin_schema,
            cv.Required(CONF_FREQUENCY): cv.int_range(min=137000000, max=1020000000),
            cv.Required(CONF_MODULATION): cv.enum(MOD),
            cv.Optional(CONF_RX_FLOOR, default=-94): cv.float_range(min=-128, max=-1),
            cv.Optional(CONF_RX_START, default=True): cv.boolean,
            cv.Optional(CONF_RX_BANDWIDTH, default="50_0kHz"): cv.enum(RX_BW),
            cv.Optional(CONF_PA_PIN, default="PA_BOOST"): cv.enum(PA_PIN),
            cv.Optional(CONF_PA_POWER, default=17): cv.int_range(min=0, max=17),
            cv.Optional(CONF_TRANSMITTER_ID): cv.use_id(remote_transmitter.RemoteTransmitterComponent),
        }
    ).extend(spi.spi_device_schema(False, 8e6, 'mode0'))
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await spi.register_spi_device(var, config)
    rst_pin = await cg.gpio_pin_expression(config[CONF_RST_PIN])
    cg.add(var.set_rst_pin(rst_pin))
    nss_pin = await cg.gpio_pin_expression(config[CONF_NSS_PIN])
    cg.add(var.set_nss_pin(nss_pin))
    cg.add(var.set_frequency(config[CONF_FREQUENCY]))
    cg.add(var.set_modulation(config[CONF_MODULATION]))
    cg.add(var.set_rx_floor(config[CONF_RX_FLOOR]))
    cg.add(var.set_rx_start(config[CONF_RX_START]))
    cg.add(var.set_rx_bandwidth(config[CONF_RX_BANDWIDTH]))
    cg.add(var.set_pa_pin(config[CONF_PA_PIN]))
    cg.add(var.set_pa_power(config[CONF_PA_POWER]))
    if config.get(CONF_TRANSMITTER_ID):
        tx = await cg.get_variable(config[CONF_TRANSMITTER_ID])
        cg.add(var.set_transmitter(tx))
