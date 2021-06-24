/*
 * Parent SST model
 *
 * */

#include <sst/core/component.h>
#include <sst/core/interfaces/stringEvent.h>
#include <sst/core/link.h>

class calculator : public SST::Component {
public:
    calculator(SST::ComponentId_t, SST::Params&);

    void setup() override;

    void finish() override;

    void handle_add_of_dout(SST::Event*);

    void handle_sum_dout(SST::Event*);

    bool tick(SST::Cycle_t);

    // Register the component
    SST_ELI_REGISTER_COMPONENT(calculator, // class
                               "calculator", // element library
                               "calculator", // component
                               SST_ELI_ELEMENT_VERSION(1, 0, 0),
                               "SST parent model",
                               COMPONENT_CATEGORY_UNCATEGORIZED)

    // Port name, description, event type
    SST_ELI_DOCUMENT_PORTS({"add_opand1", "Operand 1", {"sst.Interfaces.StringEvent"}},
                           {"add_opand2", "Operand 2", {"sst.Interfaces.StringEvent"}},
                           {"sum_dout", "Sum", {"sst.Interfaces.StringEvent"}},
                           {"add_of_dout", "Overflow", {"sst.Interfaces.StringEvent"}}, )

private:
    std::string m_clock;
    SST::Link *add_opand1_link, *add_opand2_link, *sum_dout_link, *add_of_dout_link;

    // SST parameters
    SST::Output m_output;
};

calculator::calculator(SST::ComponentId_t id, SST::Params& params)
    : SST::Component(id)
    , m_clock(params.find<std::string>("clock", ""))
    , add_opand1_link(configureLink("add_opand1"))
    , add_opand2_link(configureLink("add_opand2"))
    , add_of_dout_link(
          configureLink("add_of_dout",
                        new SST::Event::Handler<calculator>(this, &calculator::handle_add_of_dout)))
    , sum_dout_link(configureLink(
          "sum_dout", new SST::Event::Handler<calculator>(this, &calculator::handle_sum_dout))) {
    m_output.init("\033[34mparent-" + getName() + "\033[0m -> ", 1, 0, SST::Output::STDOUT);

    if(!(add_opand1_link && add_opand2_link && sum_dout_link && add_of_dout_link)) {
        m_output.fatal(CALL_INFO, -1, "Failed to configure port\n");
    }

    registerClock(m_clock, new SST::Clock::Handler<calculator>(this, &calculator::tick));

    // Tell SST to wait until we authorize it to exit
    registerAsPrimaryComponent();
    primaryComponentDoNotEndSim();
}

void calculator::setup() {
    m_output.verbose(CALL_INFO, 1, 0, "Component is being set up.\n");
}

void calculator::finish() {
    m_output.verbose(CALL_INFO, 1, 0, "Destroying %s...\n", getName().c_str());
}

void calculator::handle_add_of_dout(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if(se) {
        m_output.verbose(CALL_INFO, 1, 0, "OF %s...\n", se->getString().c_str());
    }
    delete ev;
}

void calculator::handle_sum_dout(SST::Event* ev) {
    auto* se = dynamic_cast<SST::Interfaces::StringEvent*>(ev);
    if(se) {
        m_output.verbose(CALL_INFO, 1, 0, "SUM %s...\n", se->getString().c_str());
    }
    delete ev;
}

bool calculator::tick(SST::Cycle_t current_cycle) {

    add_opand1_link->send(new SST::Interfaces::StringEvent("5"));
    add_opand2_link->send(new SST::Interfaces::StringEvent("4"));

    return false;
}
