/*
 * Parent SST model
 *
 * */

#include <sst/core/component.h>
#include <sst/core/interfaces/stringEvent.h>
#include <sst/core/link.h>

class AdderSubtractor : public SST::Component {
public:
    AdderSubtractor(SST::ComponentId_t, SST::Params&);

    void setup() override;

    void finish() override;

    void handle_as_cout_0(SST::Event*);

    void handle_as_sum_0(SST::Event*);

    void handle_as_cout_1(SST::Event*);

    void handle_as_sum_1(SST::Event*);

    void handle_as_cout_2(SST::Event*);

    void handle_as_sum_2(SST::Event*);

    void handle_as_cout_3(SST::Event*);

    void handle_as_sum_3(SST::Event*);

    bool tick(SST::Cycle_t);

    // Register the component
    SST_ELI_REGISTER_COMPONENT(AdderSubtractor, // class
                               "calculator", // element library
                               "addersubtractor", // component
                               SST_ELI_ELEMENT_VERSION(1, 0, 0),
                               "SST parent model",
                               COMPONENT_CATEGORY_UNCATEGORIZED)

    // Port name, description, event type
    SST_ELI_DOCUMENT_PORTS(
        {"as_opand1_0", "Operand 1 (0) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand1_1", "Operand 1 (1) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand1_2", "Operand 1 (2) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand1_3", "Operand 1 (3) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},

        {"as_opand2_0", "Operand 2 (0) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand2_1", "Operand 2 (1) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand2_2", "Operand 2 (2) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_opand2_3", "Operand 2 (3) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},

        {"as_cin_0", "Carry-in of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},

        {"as_sum_0", "Sum (0) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_sum_1", "Sum (1) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_sum_2", "Sum (2) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},
        {"as_sum_3", "Sum (3) of Adder-Subtractor", {"sst.Interfaces.StringEvent"}},

        {"as_cout_3", "Operand 1 of Adder-Subtractor", {"sst.Interfaces.StringEvent"}}, )

private:
    std::string m_clock;

    int num_bits_;

    std::string opand1_[4], opand2_[4], cin_0, sum_[4], cout_3;

    // SST parameters
    SST::Output m_output;

    SST::Link *as_opand1_links[4], *as_opand2_links[4], *as_cin_0_link, *as_cout_3_link,
        *as_sum_links[4];
};

AdderSubtractor::AdderSubtractor(SST::ComponentId_t id, SST::Params& params)
    : SST::Component(id), m_clock(params.find<std::string>("clock", "")),
      num_bits_(4), opand1_{"1", "1", "0", "1"}, opand2_{"0", "1", "0", "1"},
      cin_0("0"), sum_{"X", "X", "X", "X"}, cout_3("X") {

    for (int i = 0; i < num_bits_; i++) {
        as_opand1_links[i] = configureLink("as_opand1_" + std::to_string(i));
        as_opand2_links[i] = configureLink("as_opand2_" + std::to_string(i));
    }
    as_cin_0_link = configureLink("as_cin_0");

    as_sum_links[0] = configureLink(
        "as_sum_0",
        new SST::Event::Handler<AdderSubtractor>(this, &AdderSubtractor::handle_as_sum_0));
    as_sum_links[1] = configureLink(
        "as_sum_1",
        new SST::Event::Handler<AdderSubtractor>(this, &AdderSubtractor::handle_as_sum_1));
    as_sum_links[2] = configureLink(
        "as_sum_2",
        new SST::Event::Handler<AdderSubtractor>(this, &AdderSubtractor::handle_as_sum_2));
    as_sum_links[3] = configureLink(
        "as_sum_3",
        new SST::Event::Handler<AdderSubtractor>(this, &AdderSubtractor::handle_as_sum_3));
    as_cout_3_link = configureLink(
        "as_cout_3",
        new SST::Event::Handler<AdderSubtractor>(this, &AdderSubtractor::handle_as_cout_3));

    m_output.init("\033[34mparent-" + getName() + "\033[0m -> ", 1, 0, SST::Output::STDOUT);

    if (!as_cin_0_link) {
        m_output.fatal(CALL_INFO, -1, "Failed to configure port\n");
    }
    if (!as_cout_3_link) {
        m_output.fatal(CALL_INFO, -1, "Failed to configure port\n");
    }
    for (int i = 0; i < num_bits_; i++) {
        if (!as_opand1_links[i]) {
            m_output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }
    for (int i = 0; i < num_bits_; i++) {
        if (!as_opand2_links[i]) {
            m_output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }
    for (int i = 0; i < num_bits_; i++) {
        if (!as_sum_links[i]) {
            m_output.fatal(CALL_INFO, -1, "Failed to configure port\n");
        }
    }

    registerClock(m_clock, new SST::Clock::Handler<AdderSubtractor>(this, &AdderSubtractor::tick));

    // Tell SST to wait until we authorize it to exit
    registerAsPrimaryComponent();
    primaryComponentDoNotEndSim();
}

void AdderSubtractor::setup() {
    m_output.verbose(CALL_INFO, 1, 0, "Component is being set up.\n");
}

void AdderSubtractor::finish() {
    m_output.verbose(CALL_INFO, 1, 0, "Destroying %s...\n", getName().c_str());

    std::cout << "OPAND1: ";
    for (int i = 3; i > -1; i--) {
        std::cout << opand1_[i];
    }

    std::cout << "\nOPAND2: ";
    for (int i = 3; i > -1; i--) {
        std::cout << opand2_[i];
    }

    std::cout << "\nCIN0:      " << cin_0;

    std::cout << "\nSUM:    ";
    for (int i = 3; i > -1; i--) {
        std::cout << sum_[i];
    }

    std::cout << "\nCOUT3:  " << cout_3 << '\n';
}

void AdderSubtractor::handle_as_sum_0(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum_[0] = se->getString();
    }
    delete ev;
}

void AdderSubtractor::handle_as_sum_1(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum_[1] = se->getString();
    }
    delete ev;
}

void AdderSubtractor::handle_as_sum_2(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum_[2] = se->getString();
    }
    delete ev;
}

void AdderSubtractor::handle_as_sum_3(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum_[3] = se->getString();
    }
    delete ev;
}
void AdderSubtractor::handle_as_cout_3(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        cout_3 = se->getString();
    }
    delete ev;
}

bool AdderSubtractor::tick(SST::Cycle_t) {

    as_opand1_links[0]->send(new SST::Interfaces::StringEvent(opand1_[0]));
    as_opand2_links[0]->send(new SST::Interfaces::StringEvent(opand2_[0]));
    as_cin_0_link->send(new SST::Interfaces::StringEvent(cin_0));

    as_opand1_links[1]->send(new SST::Interfaces::StringEvent(opand1_[1]));
    as_opand2_links[1]->send(new SST::Interfaces::StringEvent(opand2_[1]));

    as_opand1_links[2]->send(new SST::Interfaces::StringEvent(opand1_[2]));
    as_opand2_links[2]->send(new SST::Interfaces::StringEvent(opand2_[2]));

    as_opand1_links[3]->send(new SST::Interfaces::StringEvent(opand1_[3]));
    as_opand2_links[3]->send(new SST::Interfaces::StringEvent(opand2_[3]));

    return false;
}
