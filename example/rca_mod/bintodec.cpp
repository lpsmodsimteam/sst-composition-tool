/*
 * Parent SST model
 *
 * */

#include <sst/core/component.h>
#include <sst/core/interfaces/stringEvent.h>
#include <sst/core/link.h>

#include <cmath>

class BinToDec : public SST::Component {
public:
    BinToDec(SST::ComponentId_t, SST::Params&);

    void setup() override;

    void finish() override;

    void handle_sum_0(SST::Event*);

    void handle_sum_1(SST::Event*);

    void handle_sum_2(SST::Event*);

    void handle_sum_3(SST::Event*);

    bool tick(SST::Cycle_t);

    // Register the component
    SST_ELI_REGISTER_COMPONENT(BinToDec, // class
                               "calculator", // element library
                               "bintodec", // component
                               SST_ELI_ELEMENT_VERSION(1, 0, 0),
                               "SST parent model",
                               COMPONENT_CATEGORY_UNCATEGORIZED)

    // Port name, description, event type
    SST_ELI_DOCUMENT_PORTS({"sum_0", "Sum (0)", {"sst.Interfaces.StringEvent"}},
                           {"sum_1", "Sum (1)", {"sst.Interfaces.StringEvent"}},
                           {"sum_2", "Sum (2)", {"sst.Interfaces.StringEvent"}},
                           {"sum_3", "Sum (3)", {"sst.Interfaces.StringEvent"}}, )

private:
    // SST parameters
    std::string clock;

    // SST links
    SST::Link* sum_links[4];

    // other attributes
    int num_bits, decimal_result;
    std::string sum[4];
    SST::Output output;
};

BinToDec::BinToDec(SST::ComponentId_t id, SST::Params& params)
    : SST::Component(id), clock(params.find<std::string>("clock", "")), num_bits(4),
      decimal_result(0), sum{"X", "X", "X", "X"} {

    sum_links[0] =
        configureLink("sum_0", new SST::Event::Handler<BinToDec>(this, &BinToDec::handle_sum_0));
    sum_links[1] =
        configureLink("sum_1", new SST::Event::Handler<BinToDec>(this, &BinToDec::handle_sum_1));
    sum_links[2] =
        configureLink("sum_2", new SST::Event::Handler<BinToDec>(this, &BinToDec::handle_sum_2));
    sum_links[3] =
        configureLink("sum_3", new SST::Event::Handler<BinToDec>(this, &BinToDec::handle_sum_3));

    output.init("\033[34m" + getName() + "\033[0m -> ", 1, 0, SST::Output::STDOUT);

    for (int i = 0; i < num_bits; i++) {
        if (!sum_links[i]) {
            output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }

    registerClock(clock, new SST::Clock::Handler<BinToDec>(this, &BinToDec::tick));
}

void BinToDec::setup() {
    output.verbose(CALL_INFO, 1, 0, "Component is being set up.\n");
}

void BinToDec::finish() {

    for (int i = 0; i < num_bits - 1; i++) {
        if (sum[i] != "X") {
            decimal_result += std::pow(2 * std::stoi(sum[i]), i);
        }
    }
    if (sum[3] == "1") {
        decimal_result = (decimal_result << 3) - 1;
    }

    output.verbose(
        CALL_INFO, 1, 0, "Decimal value: %s%i\n", ((sum[3] == "1") ? "-" : ""), decimal_result);
    output.verbose(CALL_INFO, 1, 0, "Destroying %s...\n", getName().c_str());
}

void BinToDec::handle_sum_0(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum[0] = se->getString();
    }
    delete ev;
}

void BinToDec::handle_sum_1(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum[1] = se->getString();
    }
    delete ev;
}

void BinToDec::handle_sum_2(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum[2] = se->getString();
    }
    delete ev;
}

void BinToDec::handle_sum_3(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum[3] = se->getString();
    }
    delete ev;
}

bool BinToDec::tick(SST::Cycle_t) {

    return false;
}
