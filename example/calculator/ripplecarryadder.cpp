/*
 * Parent SST model
 *
 * */

#include <sst/core/component.h>
#include <sst/core/interfaces/stringEvent.h>
#include <sst/core/link.h>

class RippleCarryAdder : public SST::Component {
public:
    RippleCarryAdder(SST::ComponentId_t, SST::Params&);

    void setup() override;

    void finish() override;

    void handle_add_cout_0(SST::Event*);

    void handle_add_sum_0(SST::Event*);

    void handle_add_cout_1(SST::Event*);

    void handle_add_sum_1(SST::Event*);

    void handle_add_cout_2(SST::Event*);

    void handle_add_sum_2(SST::Event*);

    void handle_add_cout_3(SST::Event*);

    void handle_add_sum_3(SST::Event*);

    bool tick(SST::Cycle_t);

    // Register the component
    SST_ELI_REGISTER_COMPONENT(RippleCarryAdder, // class
                               "calculator", // element library
                               "ripplecarryadder", // component
                               SST_ELI_ELEMENT_VERSION(1, 0, 0),
                               "SST parent model",
                               COMPONENT_CATEGORY_UNCATEGORIZED)

    // Port name, description, event type
    SST_ELI_DOCUMENT_PORTS(
        {"add_opand1_0", "Operand 1 of Full Adder 0", {"sst.Interfaces.StringEvent"}},
        {"add_opand2_0", "Operand 2 of Full Adder 0", {"sst.Interfaces.StringEvent"}},
        {"add_cin_0", "Carry-in of Full Adder 0", {"sst.Interfaces.StringEvent"}},
        {"add_sum_0", "Sum of Full Adder 0", {"sst.Interfaces.StringEvent"}},
        {"add_cout_0", "Carry-out of Full Adder 0", {"sst.Interfaces.StringEvent"}},

        {"add_opand1_1", "Operand 1 of Full Adder 1", {"sst.Interfaces.StringEvent"}},
        {"add_opand2_1", "Operand 2 of Full Adder 1", {"sst.Interfaces.StringEvent"}},
        {"add_cin_1", "Carry-in of Full Adder 1", {"sst.Interfaces.StringEvent"}},
        {"add_sum_1", "Sum of Full Adder 1", {"sst.Interfaces.StringEvent"}},
        {"add_cout_1", "Carry-out of Full Adder 1", {"sst.Interfaces.StringEvent"}},

        {"add_opand1_2", "Operand 1 of Full Adder 2", {"sst.Interfaces.StringEvent"}},
        {"add_opand2_2", "Operand 2 of Full Adder 2", {"sst.Interfaces.StringEvent"}},
        {"add_cin_2", "Carry-in of Full Adder 2", {"sst.Interfaces.StringEvent"}},
        {"add_sum_2", "Sum of Full Adder 2", {"sst.Interfaces.StringEvent"}},
        {"add_cout_2", "Carry-out of Full Adder 2", {"sst.Interfaces.StringEvent"}},

        {"add_opand1_3", "Operand 1 of Full Adder 3", {"sst.Interfaces.StringEvent"}},
        {"add_opand2_3", "Operand 2 of Full Adder 3", {"sst.Interfaces.StringEvent"}},
        {"add_cin_3", "Carry-in of Full Adder 3", {"sst.Interfaces.StringEvent"}},
        {"add_sum_3", "Sum of Full Adder 3", {"sst.Interfaces.StringEvent"}},
        {"add_cout_3", "Carry-out of Full Adder 3", {"sst.Interfaces.StringEvent"}}, )

private:
    std::string m_clock;

    int num_bits_;

    std::string opand1_[4], opand2_[4], cin_[4], sum_[4], cout_[4];

    // SST parameters
    SST::Output m_output;

    SST::Link *add_opand1_links[4], *add_opand2_links[4], *add_cin_links[4], *add_sum_links[4],
        *add_cout_links[4];
};

RippleCarryAdder::RippleCarryAdder(SST::ComponentId_t id, SST::Params& params)
    : SST::Component(id), m_clock(params.find<std::string>("clock", "")), num_bits_(4),
      opand1_({"1", "1", "0", "1"}), opand2_({"0", "1", "0", "1"}), cin_({"0", "X", "X", "X"}),
      sum_({"X", "X", "X", "X"}), cout_({"X", "X", "X", "X"}) {

    for (int i = 0; i < num_bits_; i++) {
        add_opand1_links[i] = configureLink("add_opand1_" + std::to_string(i));
        add_opand2_links[i] = configureLink("add_opand2_" + std::to_string(i));
        add_cin_links[i] = configureLink("add_cin_" + std::to_string(i));
    }

    add_sum_links[0] = configureLink(
        "add_sum_0",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_sum_0));
    add_cout_links[0] = configureLink(
        "add_cout_0",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_cout_0));

    add_sum_links[1] = configureLink(
        "add_sum_1",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_sum_1));
    add_cout_links[1] = configureLink(
        "add_cout_1",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_cout_1));

    add_sum_links[2] = configureLink(
        "add_sum_2",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_sum_2));
    add_cout_links[2] = configureLink(
        "add_cout_2",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_cout_2));

    add_sum_links[3] = configureLink(
        "add_sum_3",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_sum_3));
    add_cout_links[3] = configureLink(
        "add_cout_3",
        new SST::Event::Handler<RippleCarryAdder>(this, &RippleCarryAdder::handle_add_cout_3));

    m_output.init("\033[34mparent-" + getName() + "\033[0m -> ", 1, 0, SST::Output::STDOUT);

    if (!(add_opand1_links && add_opand2_links && add_sum_links && add_cout_links)) {
        m_output.fatal(CALL_INFO, -1, "Failed to configure port\n");
    }

    registerClock(m_clock,
                  new SST::Clock::Handler<RippleCarryAdder>(this, &RippleCarryAdder::tick));

    // Tell SST to wait until we authorize it to exit
    registerAsPrimaryComponent();
    primaryComponentDoNotEndSim();
}

void RippleCarryAdder::setup() {
    m_output.verbose(CALL_INFO, 1, 0, "Component is being set up.\n");
}

void RippleCarryAdder::finish() {
    m_output.verbose(CALL_INFO, 1, 0, "Destroying %s...\n", getName().c_str());
    std::cout << "OPAND1: ";
    for (int i = 3; i > -1; i--) {
        std::cout << opand1_[i];
    }

    std::cout << "\nOPAND2: ";
    for (int i = 3; i > -1; i--) {
        std::cout << opand2_[i];
    }

    std::cout << "\nCIN:    ";
    for (int i = 3; i > -1; i--) {
        std::cout << cin_[i];
    }

    std::cout << "\nSUM:    ";
    for (int i = 3; i > -1; i--) {
        std::cout << sum_[i];
    }

    std::cout << "\nCOUT:   ";
    for (int i = 3; i > -1; i--) {
        std::cout << cout_[i];
    }
    std::cout << '\n';
}

void RippleCarryAdder::handle_add_cout_0(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        cout_[0] = se->getString();
        add_cin_links[1]->send(new SST::Interfaces::StringEvent(cout_[0]));
    }
    delete ev;
}

void RippleCarryAdder::handle_add_sum_0(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum_[0] = se->getString();
    }
    delete ev;
}

void RippleCarryAdder::handle_add_cout_1(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        cout_[1] = se->getString();
        cin_[1] = cout_[0];
        add_cin_links[2]->send(new SST::Interfaces::StringEvent(cout_[1]));
    }
    delete ev;
}

void RippleCarryAdder::handle_add_sum_1(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum_[1] = se->getString();
    }
    delete ev;
}

void RippleCarryAdder::handle_add_cout_2(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        cout_[2] = se->getString();
        cin_[2] = cout_[1];
        add_cin_links[3]->send(new SST::Interfaces::StringEvent(cout_[2]));
    }
    delete ev;
}

void RippleCarryAdder::handle_add_sum_2(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum_[2] = se->getString();
    }
    delete ev;
}

void RippleCarryAdder::handle_add_cout_3(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        cout_[3] = se->getString();
        cin_[3] = cout_[2];
    }
    delete ev;
}

void RippleCarryAdder::handle_add_sum_3(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if (se) {
        sum_[3] = se->getString();
    }
    delete ev;
}

bool RippleCarryAdder::tick(SST::Cycle_t) {

    add_opand1_links[0]->send(new SST::Interfaces::StringEvent(opand1_[0]));
    add_opand2_links[0]->send(new SST::Interfaces::StringEvent(opand2_[0]));
    add_cin_links[0]->send(new SST::Interfaces::StringEvent(cin_[0]));

    add_opand1_links[1]->send(new SST::Interfaces::StringEvent(opand1_[1]));
    add_opand2_links[1]->send(new SST::Interfaces::StringEvent(opand2_[1]));

    add_opand1_links[2]->send(new SST::Interfaces::StringEvent(opand1_[2]));
    add_opand2_links[2]->send(new SST::Interfaces::StringEvent(opand2_[2]));

    add_opand1_links[3]->send(new SST::Interfaces::StringEvent(opand1_[3]));
    add_opand2_links[3]->send(new SST::Interfaces::StringEvent(opand2_[3]));

    return false;
}
